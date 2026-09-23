from django.urls import path
from . import views

urlpatterns = [
    # Ruta principal para el listado
    path('', views.listar_motos, name='listar_motos'),
    
    # Ruta para crear registro
    path('crear/', views.crear_moto, name='crear_moto'),
    
    # Rutas para editar y eliminar mediante ID
    path('editar/<int:id>/', views.editar_moto, name='editar_moto'),
    path('eliminar/<int:id>/', views.eliminar_moto, name='eliminar_moto'),
]