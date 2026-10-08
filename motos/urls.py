from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import LoginApiView

urlpatterns = [
    # ---  RUTAS DE SEGURIDAD (LOGIN / LOGOUT) ---
    path('login/', auth_views.LoginView.as_view(template_name='motos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),

    # Portada principal
    path('', views.inicio, name='inicio'), 
    
    # Catálogo (CRUD)
    path('inventario/', views.listar_motos, name='listar_motos'), 
    
    # Resto de las rutas
    path('crear/', views.crear_moto, name='crear_moto'),
    path('editar/<int:id>/', views.editar_moto, name='editar_moto'),
    path('eliminar/<int:id>/', views.eliminar_moto, name='eliminar_moto'),
    
    # Ruta del API Login con Tokens que enseñó el profesor
    path('api/login/', LoginApiView.as_view(), name='api_login'),
]