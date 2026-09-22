from django.db import models

# Create your models here.
from django.db import models

class Motocicleta(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField(verbose_name="Año")
    precio = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.anio})"