import pytest
from unittest.mock import patch

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from .models import Cart, CartItem
from book.models import Book
from category.models import Category
from cart.tasks import release_book_from_cart


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(email="user@example.com", password="password")


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(email="admin@example.com", password="admin")


@pytest.fixture
def book(db):
    category = Category.objects.create(name="Fiction")
    return Book.objects.create(
        title="Test Book",
        author="Author",
        year_published=2021,
        category=category,
        stock=10,
        price=19.99,
    )


@pytest.fixture
def cart(user, db):
    return Cart.objects.create(user=user)


@pytest.fixture
def cart_item(cart, book, db):
    return CartItem.objects.create(cart=cart, book=book, quantity=1)


def test_retrieve_cart(api_client, user, cart):
    api_client.force_authenticate(user=user)
    url = reverse("cart")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"] == user.id


def test_add_to_cart(api_client, user, book):
    api_client.force_authenticate(user=user)
    url = reverse("add-to-cart", kwargs={"book_id": book.id})
    response = api_client.post(url)
    assert response.status_code == status.HTTP_201_CREATED
    assert CartItem.objects.filter(cart__user=user, book=book).exists()


def test_remove_from_cart(api_client, user, cart_item):
    api_client.force_authenticate(user=user)
    url = reverse("remove-from-cart", kwargs={"book_id": cart_item.book.id})
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert not CartItem.objects.filter(pk=cart_item.pk).exists()


def test_checkout(api_client, user, cart_item):
    if cart_item.book.stock >= cart_item.quantity:
        cart_item.book.stock -= cart_item.quantity
        cart_item.book.save(update_stock=True)

    api_client.force_authenticate(user=user)
    url = reverse("checkout")
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK, "Checkout should be successful"
    cart = Cart.objects.filter(user=user).first()
    assert cart
    assert not cart.items.exists()


@pytest.mark.django_db
def test_release_book_from_cart_success(cart_item):
    release_book_from_cart(cart_item.id)
    assert not CartItem.objects.filter(id=cart_item.id).exists()


@pytest.mark.django_db
def test_release_book_from_cart_nonexistent():
    non_existent_id = 9999
    with patch("cart.tasks.logger") as mock_logger:
        release_book_from_cart(non_existent_id)
        mock_logger.warning.assert_called_with(
            f"Cart item with ID {non_existent_id} does not exist."
        )


@pytest.mark.django_db
def test_release_book_from_cart_exception(cart_item):
    with patch(
        "cart.models.CartItem.objects.get", side_effect=Exception("Test Error")
    ), patch("cart.tasks.logger") as mock_logger:
        release_book_from_cart(cart_item.id)
        mock_logger.error.assert_called()
