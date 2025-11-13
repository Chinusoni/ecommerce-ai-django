from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("feedback/", views.feedback_view, name="feedback"),
    path("recommendations/", views.recommendations_api, name="recommendations_api"),
]
