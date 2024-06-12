from django.conf import settings
from django.db import models

from book.models import Book


class Cart(models.Model):
    """
    Represents a shopping cart associated with a user.

    Attributes:
        user (OneToOneField): The user to whom the cart belongs.
        created_at (DateTimeField): The date and time when the cart was created.
        updated_at (DateTimeField): The date and time when the cart was last updated.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.email}"


class CartItem(models.Model):
    """
    Represents an item in a shopping cart.

    Attributes:
        cart (ForeignKey): The cart to which the item belongs.
        book (ForeignKey): The book that is in the cart.
        quantity (PositiveIntegerField): The quantity of the book in the cart.
        added_at (DateTimeField): The date and time when the item was added to the cart.
    """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "book")

    def __str__(self):
        return f"{self.quantity} x {self.book.title} in {self.cart.user.email}'s Cart"
