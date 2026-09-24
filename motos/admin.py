from django.contrib import admin
from .models import Motocicleta

@admin.register(Motocicleta)
class MotocicletaAdmin(admin.ModelAdmin):
    # Columnas que se verán en el panel de administrador
    list_display = ('marca', 'modelo', 'anio', 'precio', 'stock')
    # Permite buscar motos por marca o modelo
    search_fields = ('marca', 'modelo')
    # Permite filtrar en el menú lateral por marca o año
    list_filter = ('marca', 'anio')