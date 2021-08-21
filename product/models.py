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
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def total_stock(self):
        product_stock = self.product_stock.all()
        total = sum([item.total_stock_entries for item in product_stock])
        return total

    @property
    def total_price(self):
        product_stock = self.product_stock.all()
        total = sum([item.total_stock_price for item in product_stock])
        return total


class ProductStock(models.Model):
    product = models.ForeignKey(
        Product, related_name='product_stock', on_delete=models.CASCADE, null=True, blank=True)
    init_stock = models.IntegerField(default=0, null=True, blank=True)
    real_stock = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    state = models.BooleanField(default=False)
    medium_value = models.IntegerField(default=30, null=True, blank=True)
    minium_value = models.IntegerField(default=15, null=True, blank=True)
    stock_total = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.product) + self.created_at.strftime('%m/%d/%Y, %H:%M:%S')

    # Get current total stock of object ProductStock
    # Total stock is the stock sum of every ProductEntry
    # The value of this property change if ProductEntry change
    @property
    def total_stock(self):
        product_entries = self.product_entry.all()
        total = sum([item.stock for item in product_entries])
        return total

    # Get total stock that has been recorded throughout the month
    @property
    def total_stock_entries(self):
        product_entries = self.product_entry.all()
        total = sum([item.init_stock for item in product_entries])
        return total

    # Get total stock price that has been recorded throughout the month
    @property
    def total_stock_price(self):
        product_entries = self.product_entry.all()
        total = sum([item.total_cost for item in product_entries])
        return total

    # Get difference between total_stock and real_stock.
    @property
    def difference_stock(self):
        return self.total_stock - self.real_stock

    # Get current price of object ProductStock
    # This the price of the last ProductEntry added
    @property
    def current_price(self):
        product_entry = self.product_entry.latest('created_at')
        return product_entry.unit_price

    def clean(self):
        if not self.id:
            today = datetime.today()
            queryset = ProductStock.objects.filter(product=self.product).filter(
                created_at__year=today.year, created_at__month=today.month)
            if queryset.exists():
                raise ValidationError(
                    'There is another product stock in the current month.')

    def save(self, *args, **kwargs):
        product_entry = self.product_entry.all()
        total = sum([item.stock for item in product_entry])
        self.stock_total = total
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

    # Total cost of this entry.
    # is how much money has been spent on this entry
    @property
    def total_cost(self):
        return self.unit_price * self.init_stock
