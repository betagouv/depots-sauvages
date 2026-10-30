import json
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_chatbot_chat_mock_endpoint(client):
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
def test_chatbot_chat_mock_general_question(client):
    url = reverse("chatbot-chat")
    payload = {
        "messages": [{"role": "user", "content": "Quels sont les délais légaux ?"}],
    }

    response = client.post(
        url,
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    chunks = list(response.streaming_content)
    content_str = "".join([c.decode("utf-8") for c in chunks])

    assert "text-start" in content_str
    deltas = []
    for line in content_str.split("\n"):
        if line.startswith("data: "):
            try:
                evt = json.loads(line[6:])
                if evt.get("type") == "text-delta":
                    deltas.append(evt.get("delta", ""))
            except Exception:
                pass
    reconstructed_text = "".join(deltas).lower()
    assert "mise en demeure" in reconstructed_text
