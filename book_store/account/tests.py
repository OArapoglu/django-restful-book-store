from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password
from .models import CustomUser


class AccountTests(APITestCase):
    def setUp(self):
        self.test_user = CustomUser.objects.create(
            email="test@example.com", password=make_password("testpassword123")
        )

    def test_register_user(self):
        """
        Ensure we can create a new user.
        """
        url = reverse("register_user")
        data = {"email": "newuser@example.com", "password": "newpassword123"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(
            CustomUser.objects.get(email="newuser@example.com").email,
            "newuser@example.com",
        )

    def test_register_user_with_existing_email(self):
        """
        Ensure we cannot create a user with an already existing email.
        """
        url = reverse("register_user")
        data = {"email": "test@example.com", "password": "testpassword123"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_with_incomplete_data(self):
        """
        Ensure that registration with incomplete data is not allowed.
        """
        url = reverse("register_user")
        data = {"email": "incomplete@example.com"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        """
        Ensure we can login a user with correct credentials.
        """
        url = reverse("login_user")
        data = {"email": "test@example.com", "password": "testpassword123"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_user_with_wrong_credentials(self):
        """
        Ensure user cannot login with wrong credentials.
        """
        url = reverse("login_user")
        data = {"email": "test@example.com", "password": "wrongpassword"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
