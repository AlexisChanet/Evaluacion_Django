# Importamos la base de datos de Django
from django.db import models
# Importamos los validadores para proteger la base de datos de entradas inválidas
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
import datetime

# Esta clase crea la tabla 'Motocicleta' en MySQL
class Motocicleta(models.Model):
    
    # CharField es para textos. 
    # max_length=50 y el validador aseguran que MySQL no acepte textos maliciosos o demasiado largos.
    marca = models.CharField(max_length=50, validators=[MaxLengthValidator(50)])
    modelo = models.CharField(max_length=50, validators=[MaxLengthValidator(50)])
    
    # IntegerField es para números enteros. 
    # MinValueValidator(1900) bloquea años antiguos/negativos y MaxValueValidator limita al próximo año.
    anio = models.IntegerField(
        validators=[
            MinValueValidator(1900), 
            MaxValueValidator(datetime.date.today().year + 1)
        ]
    )
    
    # MinValueValidator(1) asegura que el precio sea válido (mayor a cero) y MaxValueValidator hasta 10 millones.
    precio = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10000000)
        ]
    )
    
    # MinValueValidator(0) evita números negativos y MaxValueValidator(100) limita el stock como en tu form.
    stock = models.IntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(100)
        ]
    )

    # Esta función hace que en el panel de administración se lea "Yamaha MT-07" en vez de un genérico "Objeto 1"
    def __str__(self):
        return f"{self.marca} {self.modelo}"