from django.contrib import admin

# Register your models here.
from product.models import Product, Type, Unit

admin.site.register(Product)
admin.site.register(Type)
admin.site.register(Unit)
