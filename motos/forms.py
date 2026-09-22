from django import forms
from .models import Motocicleta

class MotocicletaForm(forms.ModelForm):
    class Meta:
        model = Motocicleta
        fields = ['marca', 'modelo', 'anio', 'precio', 'stock']
        # Los widgets le agregan la clase 'form-control' para que luego se vean bonitos con Bootstrap
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Yamaha'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. MT-07'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 2024'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio en pesos'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad disponible'}),
        }

    # Validación 1: Precio mayor a cero
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return precio

    # Validación 2: Stock no negativo
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError("El stock no puede ser un número negativo.")
        return stock