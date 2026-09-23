from django.shortcuts import render, redirect, get_object_or_404
from .models import Motocicleta
from .forms import MotocicletaForm

# READ: Muestro la página principal con el listado completo de motos.
def listar_motos(request):
    # Le pido a la base de datos que me traiga todas las motocicletas guardadas.
    motos = Motocicleta.objects.all()
    # Agregué 'motos/' a la ruta para que Django encuentre el archivo en tu carpeta.
    return render(request, 'motos/listar.html', {'motos': motos})

# CREATE: Muestro el formulario vacío y guardo los datos nuevos.
def crear_moto(request):
    if request.method == 'POST':
        # Recibo los datos que el usuario escribió en el formulario web.
        form = MotocicletaForm(request.POST)
        if form.is_valid():
            form.save() # Guardo la moto físicamente en MySQL.
            return redirect('listar_motos') # Lo devuelvo al listado si todo salió bien.
    else:
        # Si la petición es GET (solo entró a la página), muestro el formulario en blanco.
        form = MotocicletaForm()
    
    # Agregué 'motos/' a la ruta.
    return render(request, 'motos/crear.html', {'form': form})

# UPDATE: Muestro el formulario lleno y guardo los cambios de una moto específica.
def editar_moto(request, id):
    # Busco la moto exacta por su ID. Si alguien pone un ID falso en la URL, muestro error 404.
    moto = get_object_or_404(Motocicleta, id=id)
    
    if request.method == 'POST':
        # Le paso los datos nuevos y le indico a Django qué moto específica estoy actualizando (instance=moto).
        form = MotocicletaForm(request.POST, instance=moto)
        if form.is_valid():
            form.save() # Actualizo el registro en MySQL.
            return redirect('listar_motos')
    else:
        # Muestro el formulario ya lleno con los datos actuales de la moto extraídos de la base de datos.
        form = MotocicletaForm(instance=moto)
    
    # Agregué 'motos/' a la ruta. Uso un HTML distinto para editar, cumpliendo la rúbrica.
    return render(request, 'motos/editar.html', {'form': form})

# DELETE: Borro una moto de la base de datos.
def eliminar_moto(request, id):
    # Busco la moto por su ID y ejecuto el comando para eliminarla de MySQL.
    moto = get_object_or_404(Motocicleta, id=id)
    moto.delete() 
    # Vuelvo a cargar la página principal con la tabla actualizada.
    return redirect('listar_motos')