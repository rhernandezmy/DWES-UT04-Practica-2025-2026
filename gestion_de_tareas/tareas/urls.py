from django.urls import path
from . import views

urlpatterns = [
    # url para ver el perfil del usuario
    path('perfil/', views.mi_perfil, name='mi_perfil'),
    # url para listar alumnos
    path('alumnos/', views.listar_alumnos, name='listar_alumnos'),
    # url para listar profesores
    path('profesores/', views.listar_profesores, name='listar_profesores'),
]