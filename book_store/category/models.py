from django.db import models


class Category(models.Model):
    """
    Represents a book category. Each category has a unique name.

    Attributes:
        name (CharField): The name of the category.
        created_at (DateTimeField): The date and time the category was created. Automatically set when the object is created.
        updated_at (DateTimeField): The date and time the category was last updated. Automatically set when the object is saved.
    """

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        """
        Return the string representation of the Category, which is its name.
        """
        return self.name
