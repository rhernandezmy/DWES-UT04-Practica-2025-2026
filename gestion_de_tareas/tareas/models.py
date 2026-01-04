import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
# Create your models here.

# Distinguir el tipo de usuario entre alumno y profesor
class tipo_usuario(AbstractUser):
    es_profesor = models.BooleanField(default=False)
    es_alumno = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username
    
class Tarea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    completada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.titulo
