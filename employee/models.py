from django.db import models

# Create your models here.

# Este modelo es el empleado. 
class Employee(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name