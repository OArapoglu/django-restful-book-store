import logging
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import CustomUser

logger = logging.getLogger(__name__)


@api_view(["POST"])
def register_user(request):
    """
    API view to register a new user.
    """
    email = request.data.get("email")
    password = request.data.get("password")

    if not all([email, password]):
        logger.warning("Attempted user registration with incomplete data.")
        return Response(
            {"error": "Both email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if CustomUser.objects.filter(email=email).exists():
        logger.info(f"Attempted registration with already existing email: {email}")
        return Response(
            {"error": "User with this email already exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = CustomUser.objects.create(email=email, password=make_password(password))
    Token.objects.create(user=user)
    logger.info(f"New user registered with email: {email}")

    return Response(
        {"message": "User created successfully."}, status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
def login_user(request):
    """
    API view to log in a user.
    """
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(email=email, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        logger.info(f"User {email} logged in successfully.")
        return Response({"token": token.key})
    else:
        logger.warning(f"Failed login attempt for email: {email}")
        return Response(
            {"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
        )
