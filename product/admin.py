from django.contrib import admin

# Register your models here.
from product.models import Product, SubProduct, Type, Unit

admin.site.register(Product)
admin.site.register(SubProduct)
admin.site.register(Type)
admin.site.register(Unit)
