from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import TipoUsuario

# Formulario de registro de usuario

class RegistroUsuarioForm(UserCreationForm):
    #  Campos adicionales para distinguir tipo de usuario con checkbox
    es_alumno = forms.BooleanField(
        label="Alumno", required=False,
        help_text="Marque si el usuario es alumno"
    )
    es_profesor = forms.BooleanField(
        label="Profesor", required=False,
        help_text="Marque si el usuario es profesor"
    )
    
    class Meta:
        model = TipoUsuario
        fields = ['username', 'email', 'es_profesor', 'es_alumno', 'password1', 'password2']
        
    def clean(self):
        cleaned_data = super().clean()
        es_profesor = cleaned_data.get('es_profesor')
        es_alumno = cleaned_data.get('es_alumno')
        
        if not es_profesor and not es_alumno:
            raise forms.ValidationError("El usuario debe ser al menos profesor o alumno.")
        
        return cleaned_data