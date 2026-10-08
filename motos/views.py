from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Motocicleta
from .forms import MotocicletaForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


# READ: Muestro la página principal con el listado completo de motos.
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate

# --- VISTAS WEB NORMALES (MVT) ---

@login_required(login_url='login')
def listar_motos(request):
    motos = Motocicleta.objects.all()
    return render(request, 'motos/listar.html', {'motos': motos})

@login_required(login_url='login')
def crear_moto(request):
    if request.method == 'POST':
        form = MotocicletaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_motos')
    else:
        form = MotocicletaForm()
    
    return render(request, 'motos/crear.html', {'form': form})

@login_required(login_url='login')
def editar_moto(request, id):
    moto = get_object_or_404(Motocicleta, id=id)
    
    if request.method == 'POST':
        form = MotocicletaForm(request.POST, instance=moto)
        if form.is_valid():
            form.save()
            return redirect('listar_motos')
    else:
        form = MotocicletaForm(instance=moto)
    
    return render(request, 'motos/editar.html', {'form': form})

@login_required(login_url='login')
def eliminar_moto(request, id):
    moto = get_object_or_404(Motocicleta, id=id)
    moto.delete() 
    return redirect('listar_motos')

def inicio(request):
    return render(request, 'motos/inicio.html')



class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()

            return Response({
                'mensaje': 'Sesión cerrada correctamente'
            }, status=status.HTTP_200_OK)

        except Token.DoesNotExist:
            return Response({
                'error': 'No existe un token para este usuario'
            }, status=status.HTTP_400_BAD_REQUEST)
# --- VISTA DE LA API (ESTILO DEL PROFESOR CON TOKEN) ---
class LoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Validar las credenciales desde JSON
        usuario = authenticate(
            username=username,
            password=password
        )

        if usuario is not None:
            token, creado = Token.objects.get_or_create(
                user=usuario
            )

            return Response({
                'mensaje': 'Autenticacion correcta',
                'usuario': usuario.username,
                'token': token.key
            }, status=status.HTTP_200_OK)

        return Response({
            'error': 'Usuario o contraseña incorrectos'
        }, status=status.HTTP_401_UNAUTHORIZED)
