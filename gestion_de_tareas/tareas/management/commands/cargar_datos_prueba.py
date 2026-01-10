from django.core.management.base import BaseCommand
from django.utils import timezone
from tareas.models import TipoUsuario, Grupo, TareaIndividual, TareaGrupo, TareaEvaluable

class Command(BaseCommand):
    help = 'Carga datos de prueba para pruebas funcionales de la app'

    def handle(self, *args, **kwargs):
        # Crear superusuario
        if not TipoUsuario.objects.filter(username='admin').exists():
            admin = TipoUsuario.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Superusuario creado'))

        # Crear profesor
        profesor, created = TipoUsuario.objects.get_or_create(
            username='profesor1',
            defaults={'es_profesor': True, 'es_alumno': False, 'email': 'profesor@example.com'}
        )
        if created:
            profesor.set_password('profesor123')
            profesor.save()
            self.stdout.write(self.style.SUCCESS('Profesor creado'))

        # Crear alumnos
        alumnos = []
        for i in range(1, 4):
            alumno, created = TipoUsuario.objects.get_or_create(
                username=f'alumno{i}',
                defaults={'es_alumno': True, 'es_profesor': False, 'email': f'alumno{i}@example.com'}
            )
            if created:
                alumno.set_password(f'alumno{i}123')
                alumno.save()
                self.stdout.write(self.style.SUCCESS(f'Alumno {i} creado'))
            alumnos.append(alumno)

        # Crear grupo
        grupo, created = Grupo.objects.get_or_create(nombre='Grupo A')
        grupo.miembros.set(alumnos)
        grupo.save()
        self.stdout.write(self.style.SUCCESS('Grupo A creado y alumnos asignados'))

        now = timezone.now()
        future = now + timezone.timedelta(days=7)

        # Crear tareas individuales
        for i, alumno in enumerate(alumnos, start=1):
            tarea_ind, created = TareaIndividual.objects.get_or_create(
                titulo=f'Tarea Individual {i}',
                defaults={
                    'descripcion': 'Descripción de prueba',
                    'creador': alumno,
                    'asignado_a': alumno,
                    'fecha_entrega': future,
                    'necesita_evaluacion': False
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Tarea Individual {i} creada'))

        # Crear tarea grupal
        tarea_grupal, created = TareaGrupo.objects.get_or_create(
            titulo='Tarea Grupal 1',
            defaults={
                'descripcion': 'Descripción grupal',
                'creador': profesor,
                'grupo': grupo,
                'fecha_entrega': future,
                'necesita_evaluacion': False
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Tarea Grupal 1 creada'))

        # Crear tarea evaluable
        for i, alumno in enumerate(alumnos, start=1):
            tarea_eval, created = TareaEvaluable.objects.get_or_create(
                titulo=f'Tarea Evaluable {i}',
                defaults={
                    'descripcion': 'Descripción evaluable',
                    'creador': profesor,
                    'asignado_a': alumno,
                    'profesor_validador': profesor,
                    'fecha_entrega': future,
                    'calificacion': None,
                    'comentarios': ''
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Tarea Evaluable {i} creada'))

        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados correctamente'))
