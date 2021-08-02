from django.contrib import admin

# Register your models here.
from service.models import Service, ServiceProductDetail

admin.site.register(Service)
admin.site.register(ServiceProductDetail)
