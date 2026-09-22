from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_motos, name='listar_motos'),
    path('crear/', views.crear_moto, name='crear_moto'),
    path('editar/<int:id>/', views.editar_moto, name='editar_moto'),
    path('eliminar/<int:id>/', views.eliminar_moto, name='eliminar_moto'), # <-- Nueva ruta
]