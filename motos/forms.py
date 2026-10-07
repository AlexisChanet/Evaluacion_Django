from django import forms
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
import datetime
from .models import Motocicleta

class MotocicletaForm(forms.ModelForm):
    
    # 1. VALIDACIONES DE FORMATO (Rúbrica: Impedir datos inválidos)
    marca = forms.CharField(
        max_length=50, # Alineado con models.py
        validators=[RegexValidator(r'^[a-zA-Z0-9\s]+$', 'Solo letras y números, sin caracteres extraños.')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Yamaha'})
    )
    
    modelo = forms.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[a-zA-Z0-9\s\-]+$', 'Solo letras, números y guiones permitidos.')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: MT-07'})
    )

    # 2. REGLAS DE NEGOCIO: AÑO
    anio = forms.IntegerField(
        label="AÑO",
        validators=[
            MinValueValidator(1900, message="El año no puede ser menor a 1900."),
            # Calculamos dinámicamente el año actual + 1 para que el sistema no caduque
            MaxValueValidator(datetime.date.today().year + 1, message="Ingresa un año válido y real.")
        ],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    # El precio entra como texto para que el usuario pueda escribir "1.500.000" con puntos
    precio = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ej: 1500000',
            'oninput': 'formatearMiles(this)'
        })
    )

    # 3. REGLAS DE NEGOCIO: STOCK
    stock = forms.IntegerField(
        validators=[MinValueValidator(0, message="El stock no puede ser negativo, mínimo 0.")],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    # Conexión con el Modelo Fuerte (Active Record de Martin Fowler)
    class Meta:
        model = Motocicleta
        fields = ['marca', 'modelo', 'anio', 'precio', 'stock']

    # --- MÉTODOS CLEAN: LIMPIEZA Y TRANSFORMACIÓN DE DATOS ANTES DE GUARDAR ---

    def clean_marca(self):
        # Quitamos espacios extra y ponemos la primera letra en mayúscula (ej: " yamaha " -> "Yamaha")
        marca = self.cleaned_data.get('marca')
        return marca.strip().title() if marca else marca

    def clean_modelo(self):
        # Quitamos espacios extra y convertimos todo a mayúsculas (ej: " mt-07 " -> "MT-07")
        modelo = self.cleaned_data.get('modelo')
        return modelo.strip().upper() if modelo else modelo

    def clean_precio(self):
        # Rúbrica: "Entregar retroalimentación comprensible". 
        # Tomamos el string "1.500.000", le quitamos los puntos, y lo convertimos a número entero para MySQL
        precio_str = str(self.cleaned_data.get('precio', ''))
        precio_limpio = precio_str.replace('.', '')
        
        try:
            precio = int(precio_limpio)
        except ValueError:
            # Si escriben letras en el precio, el backend lo rechaza
            raise forms.ValidationError("Por favor, ingresa un número válido sin letras.")
            
        if precio <= 0:
            # Regla de negocio estricta: No hay motos gratis o con precio negativo
            raise forms.ValidationError("El precio de la motocicleta debe ser mayor a cero.")
            
        return precio
        
    def clean_stock(self):
        # Doble validación de seguridad por si el frontend falla
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock