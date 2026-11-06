import json
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from backend.chatbot.context import scrub_pii, build_safe_user_context
from backend.constatations.models import Constatation
from backend.procedures.models import SuiviProcedure


def test_scrub_pii():
    text = (
        "Bonjour, je suis Jean Dupont, contactez-moi au 06 12 34 56 78 ou par "
        "mail jean.dupont@collectivite.fr. L'auteur a la plaque AB-123-CD et SIRET 123 456 789 00012."
    )
    scrubbed = scrub_pii(text)
    assert "[EMAIL_MASQUÉ]" in scrubbed
    assert "jean.dupont@collectivite.fr" not in scrubbed
    assert "[TÉL_MASQUÉ]" in scrubbed
    assert "06 12 34 56 78" not in scrubbed
    assert "[IMMATRICULATION_MASQUÉE]" in scrubbed
    assert "AB-123-CD" not in scrubbed
    assert "[SIRET/SIREN_MASQUÉ]" in scrubbed
    assert "123 456 789 00012" not in scrubbed


@pytest.mark.django_db
def test_build_safe_user_context_primo_user():
    User = get_user_model()
    user = User.objects.create_user(username="primo", email="primo@mairie.fr")
    ctx = build_safe_user_context(user, current_path="/")
    assert ctx["is_authenticated"] is True
    assert ctx["profil_usager"] == "primo_utilisateur_sans_procedure"
    assert ctx["procedures_count"] == 0
    assert len(ctx["dossiers_recents"]) == 0


@pytest.mark.django_db
def test_build_safe_user_context_with_procedures():
    User = get_user_model()
    user = User.objects.create_user(username="maire", email="maire@test.fr")
    proc = Constatation.objects.create(
        user=user,
        commune="Commune Secrète",
        auteur_nom="Nom Confidentiel",
        types_depot=["Gravats"],
        volume_m3=4.5,
        auteur_identifie=True,
        is_draft=False,
    )
    suivi = proc.suivi_procedure
    suivi.lettre_envoyee = True
    suivi.ar_recu = True
    suivi.ar_statut = "non_reclame"
    suivi.save()

    ctx = build_safe_user_context(user, current_path=f"/suivi-procedure/{proc.id}")
    assert ctx["is_authenticated"] is True
    assert ctx["profil_usager"] == "utilisateur_avec_procedures"
    assert ctx["procedures_count"] == 1
    assert ctx["dossier_actif"] is not None
    assert ctx["dossier_actif"]["id"] == proc.id
    assert ctx["dossier_actif"]["volume_m3"] == 4.5
    # Strict Zero-PII check
    ctx_str = json.dumps(ctx)
    assert "Commune Secrète" not in ctx_str
    assert "Nom Confidentiel" not in ctx_str


@pytest.mark.django_db
def test_chatbot_chat_requires_authentication(client):
    url = reverse("chatbot-chat")
    payload = {"messages": [{"role": "user", "content": "Question anonyme"}]}
    response = client.post(url, data=json.dumps(payload), content_type="application/json")
    assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


@pytest.mark.django_db
def test_chatbot_chat_mock_endpoint_authenticated(client):
    User = get_user_model()
    user = User.objects.create_user(username="agent_test", email="agent@test.fr")
    client.force_login(user)

    url = reverse("chatbot-chat")
    payload = {
        "messages": [
            {"role": "user", "content": "J'ai un problème de gravats déposés à Rennes"}
        ],
        "context": {"currentPath": "/"},
    }

    response = client.post(
        url,
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "text/event-stream" in response["Content-Type"]

    chunks = list(response.streaming_content)
    content_str = "".join([c.decode("utf-8") for c in chunks])

    assert "text-start" in content_str
    assert "propose_constatation_draft" in content_str
    assert "Gravats" in content_str
    assert "Rennes" in content_str


@pytest.mark.django_db
def test_get_ai_adapter_openrouter():
    from backend.chatbot.models import ChatbotConfig
    from backend.chatbot.adapters import OpenAICompatibleAIAdapter, get_ai_adapter

    config = ChatbotConfig.get_solo()
    config.provider = "openrouter"
    config.model = ""
    config.base_url = ""
    config.api_key = "test-openrouter-key"
    config.save()

    adapter = get_ai_adapter()
    assert isinstance(adapter, OpenAICompatibleAIAdapter)
    assert adapter.model == "~deepseek/deepseek-v4-flash-latest"
    assert adapter.base_url == "https://openrouter.ai/api/v1"
    assert adapter.api_key == "test-openrouter-key"


def test_knowledge_retriever_search():
    from backend.chatbot.retriever import get_retriever

    retriever = get_retriever()
    assert len(retriever.documents) > 40

    # Test avec synonyme ("mettre" -> amende / calculateur)
    results = retriever.search("combien mettre amende", top_k=2)
    assert len(results) > 0
    assert any("amende" in doc["title"].lower() or "calculateur" in doc["content"].lower() for doc in results)

    # Test d'exclusion de la FAQ citoyenne
    all_sources = [d["source"] for d in retriever.documents]
    assert not any("vous_n_êtes_pas_une_collectivité" in src for src in all_sources)


@pytest.mark.django_db
def test_chatbot_config_fixture_and_singleton():
    from django.core.management import call_command
    from backend.chatbot.models import ChatbotConfig

    call_command("loaddata", "chatbot_config")
    config = ChatbotConfig.get_solo()
    assert config.pk == 1
    assert "Assistant IA officiel" in config.system_prompt
    assert config.timeout == 40


@pytest.mark.django_db
def test_get_ai_adapter_from_db_config():
    from backend.chatbot.adapters import OpenAICompatibleAIAdapter, get_ai_adapter
    from backend.chatbot.models import ChatbotConfig

    config = ChatbotConfig.get_solo()
    config.provider = "mistral"
    config.model = "mistral-large-test"
    config.api_key = "test-mistral-key"
    config.system_prompt = "Tu es un prompt personnalisé."
    config.save()

    adapter = get_ai_adapter()
    assert isinstance(adapter, OpenAICompatibleAIAdapter)
    assert adapter.model == "mistral-large-test"
    assert adapter.api_key == "test-mistral-key"
    assert adapter.system_prompt == "Tu es un prompt personnalisé."


@pytest.mark.django_db
def test_backoffice_chatbot_config_api():
    from django.contrib.auth import get_user_model
    from rest_framework.test import APIClient
    from backend.chatbot.models import ChatbotConfig

    User = get_user_model()
    admin_user = User.objects.create_superuser("admin@example.com", "admin@example.com", "password")
    regular_user = User.objects.create_user("user@example.com", "user@example.com", "password")

    client = APIClient()

    # Accès refusé pour user non staff
    client.force_authenticate(user=regular_user)
    res = client.get("/api/chatbot/config/")
    assert res.status_code == 403

    # Accès autorisé pour admin
    client.force_authenticate(user=admin_user)
    res = client.get("/api/chatbot/config/")
    assert res.status_code == 200
    assert "system_prompt" in res.data
    assert "default_system_prompt" in res.data
    assert "api_key" not in res.data  # write_only

    # Mise à jour de la configuration
    update_data = {
        "provider": "openrouter",
        "model": "deepseek/deepseek-chat",
        "api_key": "sk-or-v1-123456789",
        "system_prompt": "Prompt mis à jour",
        "timeout": 60,
    }
    res = client.put("/api/chatbot/config/", data=update_data, format="json")
    assert res.status_code == 200
    assert res.data["provider"] == "openrouter"
    assert res.data["model"] == "deepseek/deepseek-chat"
    assert res.data["timeout"] == 60
    assert res.data["has_api_key"] is True
    assert "••••" in res.data["api_key_masked"]

    config = ChatbotConfig.get_solo()
    assert config.provider == "openrouter"
    assert config.api_key == "sk-or-v1-123456789"
    assert config.system_prompt == "Prompt mis à jour"


@pytest.mark.django_db
def test_backoffice_chatbot_test_connection_endpoint(monkeypatch):
    from django.contrib.auth import get_user_model
    from rest_framework.test import APIClient
    from backend.chatbot.models import ChatbotConfig

    config = ChatbotConfig.get_solo()
    config.api_key = ""
    config.save()

    User = get_user_model()
    admin_user = User.objects.create_superuser("admin_test@example.com", "admin_test@example.com", "password")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    # Test avec provider mock
    res = client.post("/api/chatbot/test-connection/", data={"provider": "mock"}, format="json")
    assert res.status_code == 200
    assert res.data["success"] is True
    assert "Mock" in res.data["message"]

    # Test sans clé API pour un provider externe
    res = client.post("/api/chatbot/test-connection/", data={"provider": "openrouter", "api_key": ""}, format="json")
    assert res.status_code == 400
    assert "clé d'API" in res.data["error"]

    # Test avec simulation d'appel HTTP externe réussi
    class MockResponse:
        status_code = 200
        def json(self):
            return {
                "choices": [
                    {"message": {"content": "pong response"}}
                ]
            }

    import requests
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: MockResponse())

    res = client.post(
        "/api/chatbot/test-connection/",
        data={
            "provider": "openrouter",
            "api_key": "sk-dummy-key",
            "model": "deepseek/deepseek-chat",
        },
        format="json",
    )
    assert res.status_code == 200
    assert res.data["success"] is True
    assert res.data["sample_reply"] == "pong response"


@pytest.mark.django_db
def test_chatbot_debug_mode_logging(caplog):
    import logging
    from backend.chatbot.adapters import OpenAICompatibleAIAdapter

    adapter = OpenAICompatibleAIAdapter(
        api_key="test-key",
        model="test-model",
        base_url="https://api.test.com/v1",
        debug_mode=True,
    )

    with caplog.at_level(logging.INFO):
        # Tester que le debug logge les requêtes sortantes lors d'un stream_chat
        class MockStreamResponse:
            ok = True
            status_code = 200
            def iter_lines(self):
                yield b'data: {"choices": [{"delta": {"content": "Hello world"}}]}'
                yield b'data: [DONE]'
            def raise_for_status(self):
                pass

        import requests
        orig_post = requests.post
        requests.post = lambda *args, **kwargs: MockStreamResponse()
        try:
            generator = adapter.stream_chat(messages=[{"role": "user", "content": "Question de test"}])
            list(generator)
        finally:
            requests.post = orig_post

    assert "[CHATBOT AI DEBUG REQUEST]" in caplog.text
    assert "test-model" in caplog.text
    assert "Question de test" in caplog.text
    assert "[CHATBOT AI DEBUG RESPONSE]" in caplog.text
    assert "Hello world" in caplog.text







