from django.contrib import admin

# Register your models here.
from product.models import Product, ProductEntry, ProductStock, Type, Unit

admin.site.register(Product)
admin.site.register(ProductStock)
admin.site.register(ProductEntry)
admin.site.register(Type)
admin.site.register(Unit)
