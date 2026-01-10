from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import TareaEvaluable, TareaGrupo, TareaIndividual, TipoUsuario, Grupo
from django.utils import timezone
from django.forms import DateTimeInput

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
    
# Formulario para crear tarea individual
class TareaIndividualForm(forms.ModelForm):
    class Meta:
        model = TareaIndividual
        fields = ['titulo', 'descripcion', 'fecha_entrega', 'asignado_a', 'necesita_evaluacion']
        widgets = {
            'fecha_entrega': DateTimeInput(attrs={'type': 'datetime-local','placeholder': 'YYYY-MM-DD HH:MM'}),
        }

    def clean_fecha_entrega(self):
        fecha_entrega = self.cleaned_data.get('fecha_entrega')
        if fecha_entrega <= timezone.now():
            raise forms.ValidationError("La fecha de entrega debe ser posterior a hoy.")
        return fecha_entrega

# Formulario para crear tarea grupal
class TareaGrupoForm(forms.ModelForm):
    class Meta:
        model = TareaGrupo
        fields = ['titulo', 'descripcion', 'fecha_entrega', 'grupo']
        widgets = {
            'fecha_entrega': DateTimeInput(attrs={'type': 'datetime-local','placeholder': 'YYYY-MM-DD HH:MM'}),
        }
        
    def clean_fecha_entrega(self):
        fecha_entrega = self.cleaned_data.get('fecha_entrega')
        if fecha_entrega <= timezone.now():
            raise forms.ValidationError("La fecha de entrega debe ser posterior a hoy.")
        return fecha_entrega
    
# Formulario para crear tarea evaluable
class TareaEvaluableForm(forms.ModelForm):
    class Meta:
        model = TareaEvaluable
        fields = ['titulo', 'descripcion', 'fecha_entrega', 'asignado_a', 'profesor_validador']
        widgets = {
            'fecha_entrega': DateTimeInput(attrs={'type': 'datetime-local','placeholder': 'YYYY-MM-DD HH:MM'}),
        }
                
    def clean_fecha_entrega(self):
        fecha_entrega = self.cleaned_data.get('fecha_entrega')
        if fecha_entrega <= timezone.now():
            raise forms.ValidationError("La fecha de entrega debe ser posterior a hoy.")
        return fecha_entrega
    
# Formulario para completar tarea (común a los tres tipos)
class ValidarTareaForm(forms.ModelForm):
    class Meta:
        model = TareaEvaluable
        fields = ['calificacion', 'comentarios']