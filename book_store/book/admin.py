from django.contrib import admin

from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year_published", "price", "category", "stock")
    list_filter = ("category", "author", "year_published")
    search_fields = ("title", "author")


admin.site.register(Book, BookAdmin)
