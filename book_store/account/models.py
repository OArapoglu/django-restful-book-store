from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom User Manager for CustomUser model.

    This manager overrides the default methods for creating users and superusers,
    specifically to handle user creation where the primary identifier is the email
    address instead of a username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str, optional): The password for the user.
            **extra_fields: Additional fields for the user.

        Returns:
            CustomUser: The newly created user instance.

        Raises:
            ValueError: If no email is provided.
        """
        if not email:
            raise ValueError("The Email field must be set.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.

        Args:
            email (str): The email address of the superuser.
            password (str): The password for the superuser.
            **extra_fields: Additional fields for the superuser.

        Returns:
            CustomUser: The newly created superuser instance.

        Raises:
            ValueError: If is_staff or is_superuser is not set to True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User model that uses email as the primary identifier instead of a username.

    This model extends AbstractUser, replacing the username field with an email field for
    authentication purposes. The USERNAME_FIELD is set to 'email' to utilize email for
    logging in, and REQUIRED_FIELDS is left empty as 'email' is already required by default.
    """

    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
