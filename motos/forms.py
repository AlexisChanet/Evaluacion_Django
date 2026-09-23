from django import forms
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
import datetime
from .models import Motocicleta

class MotocicletaForm(forms.ModelForm):
    
    marca = forms.CharField(
        max_length=30,
        validators=[RegexValidator(r'^[a-zA-Z0-9\s]+$', 'Solo letras y números.')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Yamaha'})
    )
    
    modelo = forms.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[a-zA-Z0-9\s\-]+$', 'Solo letras, números y guiones.')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: MT-07'})
    )

    # Sincronizado como 'anio' para que coincida perfectamente con el modelo de base de datos
    anio = forms.IntegerField(
        label="AÑO",
        validators=[
            MinValueValidator(1900, message="El año no puede ser menor a 1900."),
            MaxValueValidator(datetime.date.today().year + 1, message="Año inválido.")
        ],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    precio = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ej: 1.500.000',
            'oninput': 'formatearMiles(this)'
        })
    )

    stock = forms.IntegerField(
        validators=[MinValueValidator(0, message="El stock no puede ser negativo.")],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Motocicleta
        fields = ['marca', 'modelo', 'anio', 'precio', 'stock']

    def clean_marca(self):
        marca = self.cleaned_data.get('marca')
        return marca.strip().title() if marca else marca

    def clean_modelo(self):
        modelo = self.cleaned_data.get('modelo')
        return modelo.strip().upper() if modelo else modelo

    def clean_precio(self):
        precio_str = str(self.cleaned_data.get('precio', ''))
        precio_limpio = precio_str.replace('.', '')
        
        try:
            precio = int(precio_limpio)
        except ValueError:
            raise forms.ValidationError("Ingrese un número válido.")
            
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a cero.")
            
        return precio
        
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock