import datetime

from rest_framework import serializers

from .models import Book
from category.models import Category


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    Provides validation for title, author, year_published, price, and stock.
    Additionally, it validates that the specified book category exists.
    """

    class Meta:
        model = Book
        fields = "__all__"

    def validate_title(self, value):
        """Check that the title is not empty."""
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_author(self, value):
        """Check that the author's name is valid."""
        if not value:
            raise serializers.ValidationError("Author name cannot be empty.")
        return value

    def validate_year_published(self, value):
        """Check that the year published is not in the future."""
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Year published cannot be in the future.")
        return value

    def validate_price(self, value):
        """Check that the price is not negative."""
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_stock(self, value):
        """Check that the stock is not negative."""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    def validate(self, data):
        """
        Perform object-level validation on the Book instance.

        Checks if the specified category in the data exists.
        """
        if (
            "category" in data
            and not Category.objects.filter(id=data["category"].id).exists()
        ):
            raise serializers.ValidationError(
                {"category": "This category does not exist."}
            )
        return data
