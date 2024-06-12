import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Book
from category.models import Category

User = get_user_model()


@pytest.mark.django_db
class TestBookViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@example.com", password="password"
        )
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="admin"
        )
        self.category = Category.objects.create(name="Fiction")
        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            year_published=2021,
            category=self.category,
            stock=10,
            price=19.99,
        )

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        assert len(response.data["results"]) == 1

    def test_filter_books_by_author(self):
        url = f"{reverse('book-list')}?author={self.book.author}"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["author"] == self.book.author

    def test_create_book_unauthorized(self):
        url = reverse("book-list")
        data = {
            "title": "New Book",
            "author": "New Author",
            "year_published": 2022,
            "category": self.category.id,
            "stock": 5,
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_book_authorized(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("book-list")
        data = {
            "title": "New Book",
            "author": "New Author",
            "year_published": 2022,
            "category": self.category.id,
            "stock": 5,
            "price": 24.99,
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_book_unauthorized(self):
        url = reverse("book-detail", kwargs={"pk": self.book.id})
        data = {"title": "Updated Book"}
        response = self.client.put(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_book_authorized(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("book-detail", kwargs={"pk": self.book.id})
        data = {
            "title": "Updated Book",
            "author": self.book.author,
            "year_published": 2022,
            "category": self.category.id,
            "price": 15.99,
        }
        response = self.client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        self.book.refresh_from_db()
        assert self.book.title == "Updated Book"

    def test_delete_book_unauthorized(self):
        assert Book.objects.filter(pk=self.book.id).exists()

        url = reverse("book-detail", kwargs={"pk": self.book.id})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_book_authorized(self):
        assert Book.objects.filter(pk=self.book.id).exists()

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("book-detail", kwargs={"pk": self.book.id})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Book.objects.filter(pk=self.book.id).exists()

    def test_stock_cannot_be_directly_edited(self):
        category = Category.objects.create(name="Test Category")
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            year_published=2020,
            category=category,
            stock=10,
            price=20.00,
        )

        book.stock = 15
        with pytest.raises(ValidationError):
            book.save()
