# DWES-UT04-Practica-2025-2026

## 1.  Objetivo principal:
* [] Creación de una aplicación para la gestión de tareas de una clase.
* [] Objetivos secundarios
* [] Modelar datos complejos con relaciones avanzadas en Django ORM
* [] Manejar formularios avanzados con validaciones customizadas
* [] Configurar y optimizar PostgreSQL en Django
* [] Aplicar migraciones con datos iniciales

## 2. Enunciado de la práctica
En esta práctica deberas desarrollar una aplicación web para la gestión de tareas en un entorno educativo que permita a profesores crear y administrar diferentes tipos de tareas, y a alumnos visualizarlas y completarlas.

* [] El sistema distinguirá entre tres tipos de tareas: individuales, grupales y evaluables,
* [] Las tareas tendrán con diferentes fórmulas para completarse según el rol de usuario: alumno o profesor.
* [] Como alumno podré crear tareas de los distintos tipos existentes.
* [] Como alumno podré validar la finalización de una tarea, que no requiera evaluación del profesor.
* [] Como profesor podré validar la finalización de tareas que lo requieran.

## 3. Listado de elementos a implementar
* Vistas

    * [] Vista en la que un alumno/profesor pueda ver sus datos.
    * [] Vista con el listado de todo el alumnado/profesorado.
    * [] Vista en la que un alumno puede ver todas las tareas que ha creado o colabora.
    * [] Vista en la que un profesor puede ver todas las tareas que requieren su validación.

* Formularios

    * [] Formulario para el alta del alumnado/profesorado.
    * [] Formulario de creación de una tarea individual (puede necesitar o no evaluación de un profesor)
    * [] Formulario de creación de una tarea grupal (puede necesitar o no evaluación de un profesor)

## 4. Modelo tareas(M)

En tareas/models.py, crear un modelo Tarea con los siguientes campos:
      Campo	                Tipo	                            Descripción

* [X] id	                UUIDField (primary key)             Identificador único
* [X] titulo	            CharField	                        Nombre o título de la tarea
* [X] descripcion	        TextField	                        Descripción detallada
* [X] completada	        BooleanField (por defecto False)	Estado de la tarea
* [X] fecha_creacion	    DateTimeField (auto_now_add=True)	Fecha de creación
* [X] fecha_recordatorio	DateTimeField	                    Fecha recordatorio

* [X] 💡Añade el método __str__() para mostrar el título de la tarea en el panel de administración.