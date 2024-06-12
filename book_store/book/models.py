from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Sum, Case, When, Value, IntegerField

from category.models import Category


class BookManager(models.Manager):
    def with_effective_stock(self):
        """
        Retrieve a queryset of books with effective stock.

        This method calculates the effective stock of each book by subtracting
        the quantity of books held in all carts from the actual stock.
        Only books with a positive effective stock are returned.
        """

        CartItem = apps.get_model("cart", "CartItem")
        total_books_in_carts = CartItem.objects.values("book").annotate(
            total_quantity=Sum("quantity")
        )
        total_books_in_carts_dict = {
            item["book"]: item["total_quantity"] for item in total_books_in_carts
        }

        return (
            self.get_queryset()
            .annotate(
                effective_stock=F("stock")
                - Sum(
                    Case(
                        When(
                            id__in=total_books_in_carts_dict.keys(),
                            then=Value(total_books_in_carts_dict.get(F("id"))),
                        ),
                        default=0,
                        output_field=IntegerField(),
                    )
                )
            )
            .filter(effective_stock__gt=0)
        )


class Book(models.Model):
    """
    Represents a book in the bookstore.

    Attributes:
        title (str): Title of the book.
        author (str): Author of the book.
        year_published (int): The year the book was published.
        price (Decimal): Price of the book.
        category (ForeignKey): Category of the book, related to Category model.
        stock (int): Stock availability of the book.
        created_at (DateTimeField): The date and time when the book was created.
        updated_at (DateTimeField): The date and time when the book was last updated.
    """

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    year_published = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="books"
    )
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

    def save(self, *args, **kwargs):
        """
        Save method overridden to prevent direct editing of stock after creation.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        update_stock = kwargs.pop("update_stock", False)

        if self.pk and not update_stock:
            original = Book.objects.get(pk=self.pk)
            if original.stock != self.stock:
                raise ValidationError("Stock cannot be edited directly.")

        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
