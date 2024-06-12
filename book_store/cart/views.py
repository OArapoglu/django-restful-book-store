import logging

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem
from .serializers import CartSerializer
from .tasks import release_book_from_cart
from book.models import Book
logger = logging.getLogger(__name__)


class CartView(generics.RetrieveAPIView):
    """
    API view for retrieving a user's cart.
    """

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Get or create a cart for the current user.
        """
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)

        if created:
            logger.info(f"New cart created for user {user.email}")
        else:
            logger.info(f"Cart retrieved for user {user.email}")

        return cart


class AddToCartView(APIView):
    """
    API view for adding a book to the user's cart.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        """
        Handle POST request to add a book to the cart.
        """
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)

        if created:
            logger.info(f"New cart created for user {user.email}")

        if CartItem.objects.filter(cart=cart, book_id=book_id).exists():
            logger.warning(
                f"User {user.email} attempted to add book {book_id} which is already in their cart"
            )
            return Response(
                {"message": "This book is already in your cart."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        book = get_object_or_404(Book, pk=book_id)

        if not Book.objects.with_effective_stock().filter(id=book.id).exists():
            logger.info(
                f"Book {book_id} not available in sufficient quantity for user {user.email}"
            )
            return Response(
                {"message": "This book is not available in sufficient quantity."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item = CartItem.objects.create(cart=cart, book=book)
        logger.info(f"Book {book_id} added to cart for user {user.email}")

        release_book_from_cart.apply_async((cart_item.id,), countdown=1800)
        return Response(
            {"message": "This book added to cart."},
            status=status.HTTP_201_CREATED,
        )


class RemoveFromCartView(APIView):
    """
    API view for removing a book from the user's cart.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        """
        Handle POST request to remove a book from the cart.
        """
        user = request.user
        cart = get_object_or_404(Cart, user=user)

        try:
            cart_item = CartItem.objects.get(cart=cart, book_id=book_id)
            cart_item.delete()
            logger.info(f"User {user.email} removed book id {book_id} from their cart.")
            return Response(
                {"message": "The book has been removed from your cart."},
                status=status.HTTP_200_OK,
            )
        except CartItem.DoesNotExist:
            logger.warning(
                f"User {user.email} attempted to remove a non-existent book id {book_id} from their cart."
            )
            return Response(
                {"message": "This book is not in your cart."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CheckoutView(APIView):
    """
    API view for checking out the cart, reducing the stock of the books.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle POST request to checkout the items in the cart.
        """
        user = request.user
        with transaction.atomic():
            cart = Cart.objects.filter(user=user).first()
            if not cart or not cart.items.exists():
                logger.info(
                    f"Checkout attempted by user {user.email} with an empty cart."
                )
                return Response(
                    {"message": "No items in the cart to checkout."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            out_of_stock_items = []
            for item in cart.items.all():
                book = item.book
                if book.stock >= item.quantity:
                    book.stock -= item.quantity
                    book.save(update_stock=True)
                else:
                    out_of_stock_items.append(book.title)

            if out_of_stock_items:
                transaction.set_rollback(True)
                logger.warning(
                    f"Checkout failed for user {user.email} due to out-of-stock items: {', '.join(out_of_stock_items)}"
                )
                return Response(
                    {
                        "message": f"Book {', '.join(out_of_stock_items)} is out of stock."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            cart.items.all().delete()
            logger.info(f"Checkout successful for user {user.email}.")
            return Response(
                {"message": "Checkout successful."}, status=status.HTTP_200_OK
            )
