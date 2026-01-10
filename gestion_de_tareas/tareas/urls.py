from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('mis_tareas/', views.mis_tareas, name='mis_tareas'),
    path('perfil/', views.mi_perfil, name='mi_perfil'),
    path('alumnos/', views.listar_alumnos, name='listar_alumnos'),
    path('profesores/', views.listar_profesores, name='listar_profesores'),
    path('tareas_a_validar/', views.tareas_a_validar, name='tareas_a_validar'),  # vista para profesores
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('crear_tarea/<str:tipo>/', views.crear_tarea, name='crear_tarea'),
    path('completar_tarea/<str:tipo>/<uuid:tarea_id>/', views.completar_tarea, name='completar_tarea'),
]