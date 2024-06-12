import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Category

User = get_user_model()


@pytest.mark.django_db
class TestCategoryViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@example.com", password="password"
        )
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="admin"
        )
        self.category = Category.objects.create(name="Fiction")

    def test_list_categories(self):
        url = reverse("category-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_retrieve_category(self):
        url = reverse("category-detail", kwargs={"pk": self.category.id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == self.category.name

    def test_create_category_unauthorized(self):
        url = reverse("category-list")
        data = {"name": "New Category"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_category_authorized(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("category-list")
        data = {"name": "New Category"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_category_unauthorized(self):
        url = reverse("category-detail", kwargs={"pk": self.category.id})
        data = {"name": "Updated Category"}
        response = self.client.put(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_category_authorized(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("category-detail", kwargs={"pk": self.category.id})
        data = {"name": "Updated Category"}
        response = self.client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        self.category.refresh_from_db()
        assert self.category.name == "Updated Category"

    def test_delete_category_unauthorized(self):
        url = reverse("category-detail", kwargs={"pk": self.category.id})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_category_authorized(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("category-detail", kwargs={"pk": self.category.id})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(pk=self.category.id).exists()
