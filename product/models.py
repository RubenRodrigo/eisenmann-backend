from django.db import models


# Create your models here.

# Este modelo es el tipo de producto: Soldadura, Pintura, etc
class Type(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


# Este modelo es la unidad del product: kg, lt, cm
class Unit(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    abr = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return self.name


# Modelo general del producto
class Product(models.Model):
    type = models.ForeignKey(
        Type, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.ForeignKey(
        Unit, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=12, null=True, blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def total_stock(self):
        product_entries = self.product_entry.all()
        total = sum([item.stock for item in product_entries])
        return total

    @property
    def current_price(self):
        product_entry = self.product_entry.latest('created_at')
        return product_entry.unit_price


# Modelo general de entrada de producto
class ProductEntry(models.Model):
    product = models.ForeignKey(
        Product, related_name='product_entry', on_delete=models.SET_NULL, null=True, blank=True)
    init_stock = models.IntegerField(default=0, null=True, blank=True)
    stock = models.IntegerField(default=0, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    unit_price = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.created_at.strftime('%m/%d/%Y, %H:%M:%S')

    @property
    def total_cost(self):
        return self.unit_price * self.init_stock
