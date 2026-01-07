import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Distinguir el tipo de usuario entre alumno y profesor
class TipoUsuario(AbstractUser):
    es_profesor = models.BooleanField(default=False)
    es_alumno = models.BooleanField(default=True)
    
    def save (self, *args, **kwargs):
        # Si es superuser-> debe tener acceso total
        if self.is_superuser:
            self.es_profesor = True
            self.es_alumno = False
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username
    
# Modelo base para tareas
class TareaBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    completada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    
    class Meta: # Indica que es una clase abstracta
        abstract = True

    def __str__(self):
        return self.titulo

# Modelo para grupos de usuarios
class Grupo(models.Model):
    nombre = models.CharField(max_length=255)
    
    miembros = models.ManyToManyField(
        TipoUsuario, 
        related_name='grupos'
    )

    def __str__(self):
        return self.nombre
    
# Modelo para tareas asignadas a grupos
class TareaGrupo(TareaBase):
    creador = models.ForeignKey(
        TipoUsuario, 
        on_delete=models.CASCADE, 
        related_name='tareas_creadas_grupo'
    )
    grupo = models.ForeignKey(
        Grupo, 
        on_delete=models.CASCADE, 
        related_name='tareas_grupo'
    )
    
    necesita_evaluacion = models.BooleanField(default=False)
    
# Modelo para tareas asignadas a usuarios individuales
class TareaIndividual(TareaBase):
    creador = models.ForeignKey(
        TipoUsuario, 
        on_delete=models.CASCADE, 
        related_name='tareas_creadas_individual'
    )
    asignado_a = models.ForeignKey(
        TipoUsuario, 
        on_delete=models.CASCADE, 
        related_name='tareas_asignadas'
    )
    
    necesita_evaluacion = models.BooleanField(default=False)
    
# Modelo para tareas evaluables
class TareaEvaluable(TareaBase):
    creador = models.ForeignKey(
        TipoUsuario, 
        on_delete=models.CASCADE, 
        related_name='tarea_creada_evaluable'
    )
    asignado_a = models.ForeignKey(
        TipoUsuario, 
        on_delete=models.CASCADE, 
        related_name='tarea_evaluable_asignada'
    )
    profesor_validador = models.ForeignKey(
        TipoUsuario, 
        on_delete=models.SET_NULL, # Mantener la tarea aunque el profesor sea eliminado
        blank=True,
        null=True,
        related_name='tarea_a_validar'
    )
    
    calificacion = models.FloatField(blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)