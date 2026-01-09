from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TareaEvaluable, TareaGrupo, TareaIndividual, TipoUsuario
from .forms import RegistroUsuarioForm
from django.db.models import Q

# Create your views here.

# Vista para la página de perfil del usuario
@login_required # Asegura que el usuario esté autenticado
def mi_perfil(request):
    usuario = request.user # Obtener el usuario autenticado
    return render(request, 'tareas/mi_perfil.html', {'usuario': usuario}) # Renderizar la plantilla con el contexto del usuario

# Vista para ver listado de alumnos (solo para profesores y superusuarios)
@login_required
def listar_alumnos(request):
    usuario = request.user
    # Solo los profesores pueden ver la lista de alumnos
    if not usuario.es_profesor:
        return render(request, 'tareas/acceso_denegado.html')  # Página de acceso denegado para no profesores ni superusuarios  

    alumnos = TipoUsuario.objects.filter(es_alumno=True)
    return render(request, 'tareas/listar_alumnos.html', {'alumnos': alumnos}) # Renderizar la plantilla con el contexto de alumnos

# Vista para ver listado de profesores
@login_required
def listar_profesores(request):
    profesores = TipoUsuario.objects.filter(es_profesor=True)
    return render(request, 'tareas/listar_profesores.html', {'profesores': profesores}) # Renderizar la plantilla con el contexto de profesores

# Vista para crear usuarios (profesores y superusuarios)
@login_required
def crear_usuario(request):
    usuario = request.user
    if not usuario.es_profesor:
        return render(request, 'tareas/acceso_denegado.html')  # Página de acceso denegado 

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'tareas/usuario_creado.html')  # Página de confirmación de usuario creado
    else:
        form = RegistroUsuarioForm()
    return render(request, 'tareas/crear_usuario.html', {'form': form})

# Vista para que muestre a los alumnos sus tareas asignadas y las creadas por ellos
# Vista para que los superusuarios les permita ver todas las tareas
@login_required
def mis_tareas(request):
    usuario = request.user

    if usuario.is_superuser:
        # Superusuario ve todas las tareas
        tareas_individuales = TareaIndividual.objects.all().order_by('fecha_entrega')
        tareas_grupales = TareaGrupo.objects.all().order_by('fecha_entrega')
        tareas_evaluables = TareaEvaluable.objects.all().order_by('fecha_entrega')

    elif usuario.es_alumno:       # Alumnos normales solo ven sus tareas
        # Tareas individuales
        tareas_individuales = TareaIndividual.objects.filter(Q(asignado_a=usuario) | Q(creador=usuario)).order_by('fecha_entrega')
    
        # Tareas grupales (a través de los grupos del usuario)
        grupos_usuario = usuario.grupos.all()
        tareas_grupales = TareaGrupo.objects.filter(Q(grupo__in=grupos_usuario) | Q(creador=usuario)).distinct().order_by('fecha_entrega')

        # Tareas evaluables
        tareas_evaluables = TareaEvaluable.objects.filter(Q(asignado_a=usuario) | Q(creador=usuario)).order_by('fecha_entrega')
        
    else:
        # Otros tipos de usuarios no tienen acceso a esta vista
        return render(request, 'tareas/acceso_denegado.html')  # Página de acceso denegado
        
    contexto = {
        'tareas_individuales': tareas_individuales,
        'tareas_grupales': tareas_grupales,
        'tareas_evaluables': tareas_evaluables,
    }
    return render(request, 'tareas/mis_tareas.html', contexto)
    
# Vista para que los profesores vean las tareas que necesitan su validación y superusuarios vean todas las tareas evaluables
@login_required
def tareas_a_validar(request):
    usuario = request.user
    
    if usuario.is_superuser:
        # Superusuario ve todas las tareas que necesitan validación
        tareas_evaluables = TareaEvaluable.objects.all()
    
    elif usuario.es_profesor:
        # Profesores ven solo las tareas que les han sido asignadas para validar
        tareas_evaluables = TareaEvaluable.objects.filter(profesor_validador=usuario)
    
    else:
        return render(request, 'tareas/acceso_denegado.html')  # Página de acceso denegado
    
    # Ordenar las tareas por fecha de entrega ascendente
    tareas_evaluables = tareas_evaluables.order_by('fecha_entrega')
    
    contexto = {
        'tareas_evaluables': tareas_evaluables,
    }
    return render(request, 'tareas/tareas_a_validar.html', contexto)

#