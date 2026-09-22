from django.shortcuts import render, redirect, get_object_or_404
from .forms import MotocicletaForm
from .models import Motocicleta 

def crear_moto(request):
    if request.method == 'POST':
        form = MotocicletaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_motos') # <-- Cambia 'crear_moto' por 'listar_motos' para que te lleve a la tabla al guardar
    else:
        form = MotocicletaForm()
    return render(request, 'motos/crear.html', {'form': form})

# --- NUEVA FUNCIÓN PARA LISTAR ---
def listar_motos(request):
    motos = Motocicleta.objects.all() # Va a MySQL y trae todas las motos
    return render(request, 'motos/listar.html', {'motos': motos})

# --- NUEVA FUNCIÓN PARA EDITAR ---
def editar_moto(request, id):
    # Busca la moto por su ID, si no existe lanza error 404
    moto = get_object_or_404(Motocicleta, id=id)
    
    if request.method == 'POST':
        # Le pasamos los datos nuevos, pero le decimos que sobreescriba la 'instance' existente
        form = MotocicletaForm(request.POST, instance=moto)
        if form.is_valid():
            form.save()
            return redirect('listar_motos')
    else:
        # Carga el formulario con los datos actuales de la moto
        form = MotocicletaForm(instance=moto)
        
    return render(request, 'motos/editar.html', {'form': form})

# --- NUEVA FUNCIÓN PARA ELIMINAR ---
def eliminar_moto(request, id):
    moto = get_object_or_404(Motocicleta, id=id)
    moto.delete() # Borra la moto de MySQL
    return redirect('listar_motos') # Recarga la tabla actualizada