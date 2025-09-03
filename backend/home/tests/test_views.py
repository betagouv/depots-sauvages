from django.urls import reverse


def test_home_page_loads_correctly(client):
    url = reverse("index")
    response = client.get(url)
    assert "Protect'Envi" in response.content.decode()
