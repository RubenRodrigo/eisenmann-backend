from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime


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
        product_stock = self.product_stock.all()
        total = sum([item.real_stock for item in product_stock])
        return total

    @property
    def current_price(self):
        product_entry = self.product_entry.latest('created_at')
        return product_entry.unit_price


class ProductStock(models.Model):
    product = models.ForeignKey(
        Product, related_name='product_stock', on_delete=models.CASCADE, null=True, blank=True)
    init_stock = models.IntegerField(default=0, null=True, blank=True)
    real_stock = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    state = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product) + self.created_at.strftime('%m/%d/%Y, %H:%M:%S')

    # Get current total stock of object ProductStock
    # Total stock is the sum of every stock in ProductEntry
    @property
    def total_stock(self):
        product_entries = self.product_entry.all()
        total = sum([item.stock for item in product_entries])
        return total

    @property
    def difference_stock(self):
        return self.total_stock - self.real_stock

    @property
    def current_price(self):
        product_entry = self.product_entry.latest('created_at')
        return product_entry.unit_price

    # Get total stock that has been recorded throughout the month
    @property
    def total_stock_entries(self):
        product_entries = self.product_entry.all()
        total = sum([item.init_stock for item in product_entries])
        return total

    def clean(self):
        today = datetime.today()
        queryset = ProductStock.objects.filter(product=self.product).filter(
            created_at__year=today.year, created_at__month=today.month)
        if queryset.exists():
            raise ValidationError(
                'There is another product stock in the current month.')

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        today = datetime.today()
        self.updated_at = today
        return super(ProductStock, self).save(*args, **kwargs)

# Modelo general de entrada de producto


class ProductEntry(models.Model):
    product = models.ForeignKey(
        ProductStock, related_name='product_entry', on_delete=models.CASCADE, null=True, blank=True)
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
