from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    Includes validation to ensure that the category name is not empty.
    """

    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):
        """
        Validate that the name field is not empty.

        Args:
            value (str): The value of the name field to be validated.

        Returns:
            str: The validated name value.

        Raises:
            serializers.ValidationError: If the name is empty.
        """
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        return value
