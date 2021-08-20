from django.db import models


# Create your models here.

# Este modelo contiene la informacion del cliente
# El cliente es la persona que solicito el servicio
class Client(models.Model):
    # tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=32, null=True, blank=True)
    identifier = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    # ultimo_servicio = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.name

    @property
    def total_services(self):
        services = self.client_services.all().count()
        return services


'''
    def save(self, *args, **kwargs):
        '' On save, update timestamps ''
        if not self.id:
            self.ultimo_servicio = timezone.now().date()
        else:
            self.ultimo_servicio = timezone.now().date()
            self.servicio_totales = self.servicio_set.all().count()
        return super(Cliente, self).save(*args, **kwargs)
'''
