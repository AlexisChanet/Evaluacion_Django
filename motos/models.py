from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
import datetime

class Motocicleta(models.Model):
    marca = models.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[a-zA-Z0-9\s]+$', 'Error: Usa solo letras y números.')]
    )
    modelo = models.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[a-zA-Z0-9\s\-]+$', 'Error: Usa solo letras, números y guiones.')]
    )
    anio = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.date.today().year + 1)
        ]
    )
    precio = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10000000)
        ]
    )
    stock = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    class Meta:
        constraints = [
            # Restricción SQL para el año (mínimo 1900 y máximo año actual + 1)
            models.CheckConstraint(
                check=models.Q(anio__gte=1900) & models.Q(anio__lte=datetime.date.today().year + 1),
                name='chk_anio_valido'
            ),
            # Restricción SQL para el stock (entre 0 y 100)
            models.CheckConstraint(
                check=models.Q(stock__gte=0) & models.Q(stock__lte=100),
                name='chk_stock_valido'
            ),
            # Restricción SQL para el precio (entre 1 y 10.000.000)
            models.CheckConstraint(
                check=models.Q(precio__gte=1) & models.Q(precio__lte=10000000),
                name='chk_precio_valido'
            ),
        ]

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.anio})"