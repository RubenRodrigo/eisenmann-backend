from django.core.exceptions import ValidationError
from employee.models import Employee
from django.db import models
from django.utils import timezone

# Create your models here.
from client.models import Client
from product.models import Product, ProductStock


# Este modelo guarda el Servicio.
class Service(models.Model):
    client = models.ForeignKey(
        Client, related_name='client_services', on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=8, null=True, blank=True)
    estimated_price = models.CharField(max_length=128, null=True, blank=True)
    init_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    observations = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.init_date = timezone.now().date()
        self.end_date = timezone.now().date()
        return super(Service, self).save(*args, **kwargs)

    @property
    def final_price(self):
        service_products = self.service_products.all()
        total = sum([item.total_cost for item in service_products])
        return total


# Este modelo guarda los productos que se guardan en un servicio
class ServiceProductDetail(models.Model):
    service = models.ForeignKey(
        Service, related_name='service_products', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        ProductStock, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    total_cost = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        return self.description

    def clean(self):
        if not self.product.product_entry.exists():
            raise ValidationError('This product has not entries.')

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.product.current_price
        return super(ServiceProductDetail, self).save(*args, **kwargs)
