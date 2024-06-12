from django.urls import path
from .views import AddToCartView, CheckoutView, CartView, RemoveFromCartView

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add-to-cart/<int:book_id>/", AddToCartView.as_view(), name="add-to-cart"),
    path(
        "remove-from-cart/<int:book_id>/",
        RemoveFromCartView.as_view(),
        name="remove-from-cart",
    ),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
]
