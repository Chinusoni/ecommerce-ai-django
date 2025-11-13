from django.contrib import admin
from .models import Product, CartItem, Feedback

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Feedback)
