from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TareaEvaluable, TareaGrupo, TareaIndividual, TipoUsuario
from django.db.models import Q
from .forms import RegistroUsuarioForm, TareaIndividualForm, TareaGrupoForm, TareaEvaluableForm, ValidarTareaForm
from django.shortcuts import get_object_or_404, redirect

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
        
    elif usuario.es_profesor:
        tareas_individuales = TareaIndividual.objects.filter(creador=usuario).order_by('fecha_entrega')
        tareas_grupales = TareaGrupo.objects.filter(creador=usuario).order_by('fecha_entrega')
        tareas_evaluables = TareaEvaluable.objects.filter(creador=usuario).order_by('fecha_entrega')

    
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
        # Superusuario ve todas las tareas evaluables no completadas
        tareas_evaluables = TareaEvaluable.objects.filter(completada=False).order_by('fecha_entrega')
    
    elif usuario.es_profesor:
        # Profesores ven solo las tareas asignadas a ellos y que no estén completadas
        tareas_evaluables = TareaEvaluable.objects.filter(
            profesor_validador=usuario,
            completada=False
        ).order_by('fecha_entrega')
    
    else:
        return render(request, 'tareas/acceso_denegado.html')
    
    contexto = {
        'tareas_evaluables': tareas_evaluables,
    }
    return render(request, 'tareas/tareas_a_validar.html', contexto)


# Vista para crear tareas (para profesores y alumnos)
@login_required
def crear_tarea(request, tipo):
    usuario = request.user

    # Solo alumnos o profesores pueden crear tareas
    if not (usuario.es_profesor or usuario.es_alumno):
        return render(request, 'tareas/acceso_denegado.html')

    # Elegir formulario según tipo de tarea
    if tipo == "individual":
        FormClass = TareaIndividualForm
    elif tipo == "grupal":
        FormClass = TareaGrupoForm
    elif tipo == "evaluable":
        FormClass = TareaEvaluableForm
    else:
        return render(request, 'tareas/acceso_denegado.html')  # Tipo no válido

    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.creador = usuario  # Siempre asignamos el creador

            # Si es alumno y la tarea es evaluable, no puede asignar profesor_validador
            if usuario.es_alumno and tipo == "evaluable":
                tarea.profesor_validador = None

            tarea.save()
            return render(request, 'tareas/tarea_creada.html', {'tarea': tarea})
    else:
        form = FormClass()
        # Para alumnos deshabilitamos el campo profesor_validador si existe
        if usuario.es_alumno and tipo == "evaluable":
            form.fields.get('profesor_validador') and setattr(form.fields['profesor_validador'], 'disabled', True)

    contexto = {
        'form': form,
        'tipo': tipo,
        'usuario': usuario,
    }
    return render(request, 'tareas/crear_tarea.html', contexto)


# Vista para completar tareas (alumnos y profesores)
@login_required
def completar_tarea(request, tipo, tarea_id):
    usuario = request.user

    if tipo == 'individual':
        tarea = get_object_or_404(TareaIndividual, id=tarea_id)

        if usuario.es_alumno and not (
            tarea.asignado_a == usuario or tarea.creador == usuario
        ):
            return render(request, 'tareas/acceso_denegado.html')

    elif tipo == 'grupal':
        tarea = get_object_or_404(TareaGrupo, id=tarea_id)

        if usuario.es_alumno and not (
            usuario in tarea.grupo.miembros.all() or tarea.creador == usuario
        ):
            return render(request, 'tareas/acceso_denegado.html')

    elif tipo == 'evaluable':
        tarea = get_object_or_404(TareaEvaluable, id=tarea_id)

        # Solo profesor o superuser
        if not (usuario.es_profesor or usuario.is_superuser):
            return render(request, 'tareas/acceso_denegado.html')

    else:
        return render(request, 'tareas/acceso_denegado.html')

    # 🔒 Restricción clave del enunciado
    if usuario.es_alumno and getattr(tarea, 'necesita_evaluacion', False):
        return render(request, 'tareas/acceso_denegado.html')

    # Marcar como completada
    tarea.completada = True
    tarea.save()

    return redirect('mis_tareas')


# Vista para el dashboard
@login_required
def dashboard(request):
    usuario = request.user
    contexto = {
        'usuario': usuario
    }
    return render(request, 'tareas/dashboard.html', contexto)


#Vista para la checklist avanzada
@login_required
def checklist_avanzado(request):
    usuario = request.user

    # ✅ Usuarios
    alumnos = TipoUsuario.objects.filter(es_alumno=True)
    profesores = TipoUsuario.objects.filter(es_profesor=True)
    superusuarios = TipoUsuario.objects.filter(is_superuser=True)

    # ✅ Tareas
    tareas_ind = TareaIndividual.objects.all()
    tareas_grup = TareaGrupo.objects.all()
    tareas_eval = TareaEvaluable.objects.all()

    # ✅ Permisos críticos
    permisos = {
        'alumno_no_evalable': False,
        'alumno_evalable': False,
        'profesor_todas': False,
        'superusuario_todas': False,
    }

    # Alumnos solo pueden completar tareas no evaluables
    tarea_ind_no_eval = tareas_ind.filter(necesita_evaluacion=False).first()
    tarea_grup_no_eval = tareas_grup.filter(necesita_evaluacion=False).first()
    tarea_eval = tareas_eval.first()

    if alumno := alumnos.first():
        permisos['alumno_no_evalable'] = True if tarea_ind_no_eval or tarea_grup_no_eval else False
        permisos['alumno_evalable'] = False  # Alumnos no pueden completar evaluables

    # Profesores pueden completar cualquier tarea
    if profesores.exists():
        permisos['profesor_todas'] = True

    # Superusuario puede completar todo
    if superusuarios.exists():
        permisos['superusuario_todas'] = True

    contexto = {
        'usuario': usuario,
        'usuarios': {
            'alumnos': alumnos.exists(),
            'profesores': profesores.exists(),
            'superusuarios': superusuarios.exists(),
        },
        'tareas': {
            'individuales': tareas_ind.exists(),
            'grupales': tareas_grup.exists(),
            'evaluables': tareas_eval.exists(),
        },
        'permisos': permisos,
    }

    return render(request, 'tareas/checklist_avanzado.html', contexto)

# Vista para validar tarea evaluable
@login_required
def validar_tarea(request, tarea_id):
    usuario = request.user
    tarea = get_object_or_404(TareaEvaluable, id=tarea_id)

    # Solo el profesor asignado o superusuario puede validar
    if not (usuario.es_profesor and tarea.profesor_validador == usuario) and not usuario.is_superuser:
        return render(request, 'tareas/acceso_denegado.html')

    if request.method == 'POST':
        form = ValidarTareaForm(request.POST, instance=tarea)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.completada = True
            form.save()
            return redirect('tareas_a_validar')
    else:
        form = ValidarTareaForm(instance=tarea)

    contexto = {
        'form': form,
        'tarea': tarea,
    }
    return render(request, 'tareas/validar_tarea.html', contexto)