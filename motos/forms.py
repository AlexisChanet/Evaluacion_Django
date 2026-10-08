from django import forms
from django.core.validators import RegexValidator
import datetime
from .models import Motocicleta

class MotocicletaForm(forms.ModelForm):
    
    marca = forms.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[a-zA-Z0-9\s]+$', 'Error: Usa solo letras y números.')],
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ej: Yamaha', 
            'maxlength': '50'
        })
    )
    
    modelo = forms.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[a-zA-Z0-9\s\-]+$', 'Error: Usa solo letras, números y guiones.')],
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ej: MT-07', 
            'maxlength': '50'
        })
    )

    anio = forms.IntegerField(
        label="AÑO",
        min_value=1900,
        max_value=datetime.date.today().year + 1,
        error_messages={
            'min_value': 'Error: El año mínimo permitido es 1900.',
            'max_value': f'Error: El año máximo es {datetime.date.today().year + 1}.'
        },
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1900',
            'max': str(datetime.date.today().year + 1),
            'onkeydown': 'return ["e", "E", "+", "-", "."].includes(event.key) ? false : true;',
            'oninput': 'if(this.value.length > 4) this.value = this.value.slice(0, 4);'
        })
    )

    precio = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ej: 1.500.000',
            'oninput': 'formatearMiles(this)',
            'maxlength': '10'
        })
    )

    stock = forms.IntegerField(
        min_value=0,
        max_value=100,
        error_messages={
            'min_value': 'Error: El stock no puede ser negativo.',
            'max_value': 'Error: La capacidad máxima de stock es 100 unidades.'
        },
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '100',
            'onkeydown': 'return ["e", "E", "+", "-", "."].includes(event.key) ? false : true;',
            'oninput': 'if(this.value.length > 3) this.value = this.value.slice(0, 3);'
        })
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
            raise forms.ValidationError("Error: Ingresa un precio numérico válido.")
            
        if precio <= 0:
            raise forms.ValidationError("Error: El precio debe ser mayor a $0.")
            
        if precio > 10000000:
            raise forms.ValidationError("Error: El precio máximo permitido es $10.000.000.")
            
        return precio