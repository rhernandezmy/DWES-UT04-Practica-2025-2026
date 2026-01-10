# DWES-UT04-Practica-2025-2026

## 1.  Objetivo principal:
* [X] Creación de una aplicación para la gestión de tareas de una clase.
* [X] Objetivos secundarios
* [X] Modelar datos complejos con relaciones avanzadas en Django ORM
* [X] Manejar formularios avanzados con validaciones customizadas
* [X] Configurar y optimizar PostgreSQL en Django
* [X] Aplicar migraciones con datos iniciales

## 2. Enunciado de la práctica
En esta práctica deberas desarrollar una aplicación web para la gestión de tareas en un entorno educativo que permita a profesores crear y administrar diferentes tipos de tareas, y a alumnos visualizarlas y completarlas.

* [X] El sistema distinguirá entre tres tipos de tareas: individuales, grupales y evaluables,
* [X] Las tareas vendrán con diferentes fórmulas para completarse según el rol de usuario: alumno o profesor.
* [X] Como alumno podré crear tareas de los distintos tipos existentes.
* [X] Como alumno podré validar la finalización de una tarea, que no requiera evaluación del profesor.
* [X] Como profesor podré validar la finalización de tareas que lo requieran.

## 3. Listado de elementos a implementar
* Vistas

    * [X] Vista en la que un alumno/profesor pueda ver sus datos.
    * [X] Vista con el listado de todo el alumnado/profesorado.
    * [X] Vista para crear usuarios (profesores y superusuarios)
    * [X] Vista en la que un alumno puede ver todas las tareas que ha creado o colabora.
    * [X] Vista en la que un profesor puede ver todas las tareas que requieren su validación.
    * [X] Vista para crear tareas (para profesores y alumnos)
    * [X] Vista para completar tareas (alumnos y profesores)
    * [X] Vista para el dashboard

* Formularios

    * [X] Formulario para el alta del alumnado/profesorado.
    * [X] Formulario de creación de una tarea individual (puede necesitar o no evaluación de un profesor)
    * [X] Formulario de creación de una tarea grupal (puede necesitar o no evaluación de un profesor)
    * [X] Formulario para crear tarea evaluable

## 4. Modelo TareaBase(M)

En tareas/models.py, crear un modelo TareaBase con los siguientes campos:
      Campo	                Tipo	                            Descripción

* [X] id	                UUIDField (primary key)               Identificador único
* [X] titulo	          CharField	                        Nombre o título de la tarea
* [X] descripcion	          TextField	                        Descripción detallada
* [X] completada	          BooleanField (por defecto False)	Estado de la tarea
* [X] fecha_creacion	    DateTimeField (auto_now_add=True)	Fecha de creación
* [X] fecha_entrega         DateTimeField	                        Fecha de entrega
* [X] fecha_completada      DateTimeField	                        Fecha de completada

* [X] 💡Añade el método __str__() para mostrar el título de la tarea en el panel de administración.

## 5. Modelo para grupos de usuarios
En tareas/models.py, crear un modelo grupos de usuarios con los siguientes campos:
      Campo	                Tipo	                            Descripción

* [X] nombre                CharField                           Nombre o título del grupo
* [X] miembros	          ManyToManyField	                Miembros del grupo

* [X] 💡Añade el método __str__() para devolver el nombre al imprimir usuario
    
## 6. Modelo para tareas asignadas a grupos
En tareas/models.py, crear un modelo TareaGrupo con los siguientes campos:
      Campo	                Tipo	                            Descripción

* [X] creador               ForeignKey                          Creador de la tarea del grupo
* [X] grupo	                ForeignKey	                      Grupo asignado a la tarea
* [X] necesita_evaluacion   BooleanField	                      Necesita evaluación por parte del profesor
    
## 7. Modelo para tareas asignadas a usuarios individuales
En tareas/models.py, crear un modelo TareaIndividual con los siguientes campos:
      Campo	                Tipo	                            Descripción

* [X] creador               ForeignKey                          Creador de la tarea del grupo
* [X] asignado_a            ForeignKey	                      Alumno asignado a la tarea
* [X] necesita_evaluacion   BooleanField	                      Necesita evaluación por parte del profesor
    
## 8. Modelo para tareas evaluables
En tareas/models.py, crear un modelo TareaEvaluable con los siguientes campos:
      Campo	                Tipo	                            Descripción

* [X] creador               ForeignKey                          Creador de la tarea del grupo
* [X] asignado_a            ForeignKey	                      Alumno asignado a la tarea
* [X] profesor_validador    ForeignKey	                      Profesor asignado como validador
* [X] calificacion	    FloatField	                      Calificación obtenida
* [X] comentarios	          TextField	                      Comentarios por parte del profesor

## 8. Usuarios creados para las pruebas
ROL           Nombre    Contraseña
Superusuario: admin     admin123

Profesor:     profesor1 profesor123

Alumnos:      alumno1   alumno1123
              alumno2   alumno2123
              alumno3   alumno3123