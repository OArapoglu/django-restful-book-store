import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Book
from .serializers import BookSerializer
from category.models import Category


class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class to define page size and limits for API responses.
    """

    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class BookFilter(django_filters.FilterSet):
    """
    Custom filter class for the Book model, allowing filtering by various fields.
    """

    categories = django_filters.ModelMultipleChoiceFilter(
        field_name="category", to_field_name="id", queryset=Category.objects.all()
    )

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "year_published",
            "categories",
        ]


class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book instances.
    """

    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    filterset_fields = [
        "title",
        "author",
        "year_published",
        "category",
    ]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Return a queryset of books, ensuring only those with effective stock are listed.
        """
        return Book.objects.with_effective_stock().order_by("title")

    def get_permissions(self):
        """
        Return the appropriate permission classes based on the action being performed.
        Actions 'list' and 'retrieve' are available to any user, while other actions
        require the user to be authenticated and to be an admin.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
