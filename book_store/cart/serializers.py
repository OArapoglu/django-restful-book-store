from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"

    def validate_quantity(self, value):
        """
        Ensure that the quantity is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate_book(self, value):
        """
        Ensure that the book is in stock.
        """
        if value.stock <= 0:
            raise serializers.ValidationError(
                f"The book {value.title} is out of stock."
            )
        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"

    def validate_items(self, value):
        """
        Validate all items in the cart.
        """
        for item in value:
            if item.quantity <= 0:
                raise serializers.ValidationError(
                    "Each item in the cart must have a positive quantity."
                )
            if item.book.stock <= 0:
                raise serializers.ValidationError(
                    f"The book {item.book.title} is out of stock."
                )
        return value
