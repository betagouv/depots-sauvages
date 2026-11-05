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


def test_get_ai_adapter_openrouter(settings):
    settings.AI_PROVIDER = "openrouter"
    settings.AI_MODEL = ""
    settings.AI_BASE_URL = ""
    settings.AI_API_KEY = "test-openrouter-key"

    from backend.chatbot.adapters import OpenAICompatibleAIAdapter, get_ai_adapter

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




