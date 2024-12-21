from django.contrib import admin

# Register your models here.
# queryapp/admin.py
from .models import Product

# Register the Product model so it appears in the Django admin interface
admin.site.register(Product)
