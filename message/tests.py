import pytest
from django.urls import reverse

from message.models import Message

pytestmark = pytest.mark.django_db


class TestMessageAPIView:
    def test_get_api(self, client):
        obj = Message.objects.create(
            name="test_name",
            content="test_content"
        )
        url = reverse("message", kwargs={"pk": obj.id})
        response = client.get(url)
        response_json = response.json()

        assert response.status_code == 200
        assert list(response_json.keys()) == ['id', 'created', 'name', 'content']
        assert response_json["name"] == "test_name"
        assert response_json["content"] == "test_content"

    def test_put_api(self, client):
        obj = Message.objects.create(
            name="test_name",
            content="test_content"
        )
        url = reverse("message", kwargs={"pk": obj.id})
        data = {"name": "changed_name", "content": "changed_content"}
        response = client.put(url, data=data)
        response_json = response.json()

        assert response.status_code == 200
        assert list(response_json.keys()) == ['id', 'created', 'name', 'content']
        assert response_json["name"] == "changed_name"
        assert response_json["content"] == "changed_content"

    def test_delete_api(self, client):
        obj = Message.objects.create(
            name="test_name",
            content="test_content"
        )
        url = reverse("message", kwargs={"pk": obj.id})
        response = client.delete(url)

        assert response.status_code == 204


    def test_post_api(self, client):
        url = reverse("messages")
        data = {"name": "created_name", "content": "created_content"}
        response = client.post(url, data=data)
        response_json = response.json()

        assert response.status_code == 201
        assert list(response_json.keys()) == ['id', 'created', 'name', 'content']
        assert response_json["name"] == "created_name"
        assert response_json["content"] == "created_content"
