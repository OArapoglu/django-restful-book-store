from django.contrib.auth.backends import ModelBackend

from .models import CustomUser


class EmailAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows users to authenticate using their email.

    This backend checks if a user with the provided email exists and, if so,
    verifies the password. If the authentication is successful, the corresponding
    user instance is returned.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticate a user based on email and password.

        Args:
            request: The HttpRequest object.
            email (str): The email address of the user attempting to authenticate.
            password (str): The password of the user.

        Returns:
            CustomUser: The authenticated user object, or None if authentication fails.
        """
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
