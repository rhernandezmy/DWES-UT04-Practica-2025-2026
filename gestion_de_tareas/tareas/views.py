from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TipoUsuario


# Create your views here.

# Vista para la página de perfil del usuario
@login_required # Asegura que el usuario esté autenticado
def mi_perfil(request):
    usuario = request.user # Obtener el usuario autenticado
    return render(request, 'tareas/mi_perfil.html', {'usuario': usuario}) # Renderizar la plantilla con el contexto del usuario

# Vista para ver listado de alumnos (solo para profesores)
@login_required
def listar_alumnos(request):
    usuario = request.user
    if not usuario.es_profesor:
        return render(request, 'tareas/acceso_denegado.html')  # Página de acceso denegado para no profesores

    alumnos = TipoUsuario.objects.filter(es_alumno=True)
    return render(request, 'tareas/listar_alumnos.html', {'alumnos': alumnos}) # Renderizar la plantilla con el contexto de alumnos

# Vista para ver listado de profesores (Para alumnos y profesores)
@login_required
def listar_profesores(request):
    usuario = request.user
    if not usuario.es_profesor and not usuario.es_alumno:
        return render(request, 'tareas/acceso_denegado.html')  # Página de acceso denegado para no profesores ni alumnos

    profesores = TipoUsuario.objects.filter(es_profesor=True)
    return render(request, 'tareas/listar_profesores.html', {'profesores': profesores}) # Renderizar la plantilla con el contexto de profesores