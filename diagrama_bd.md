```mermaid
erDiagram

    TIPOUSUARIO {
        UUID id
        string username
        string email
        boolean es_alumno
        boolean es_profesor
        boolean is_superuser
    }

    GRUPO {
        UUID id
        string nombre
    }

    TAREA_BASE {
        UUID id
        string titulo
        string descripcion
        boolean completada
        datetime fecha_creacion
        datetime fecha_entrega
    }

    TAREA_INDIVIDUAL {
        boolean necesita_evaluacion
    }

    TAREA_GRUPAL {
        boolean necesita_evaluacion
    }

    TAREA_EVALUABLE {
        float calificacion
        string comentarios
    }

    %% Relaciones de herencia
    TAREA_BASE ||--|| TAREA_INDIVIDUAL : hereda
    TAREA_BASE ||--|| TAREA_GRUPAL : hereda
    TAREA_BASE ||--|| TAREA_EVALUABLE : hereda

    %% Relaciones usuario-tarea
    TIPOUSUARIO ||--o{ TAREA_INDIVIDUAL : crea
    TIPOUSUARIO ||--o{ TAREA_GRUPAL : crea
    TIPOUSUARIO ||--o{ TAREA_EVALUABLE : crea

    TIPOUSUARIO ||--o{ TAREA_INDIVIDUAL : asignado_a
    TIPOUSUARIO ||--o{ TAREA_EVALUABLE : asignado_a

    TIPOUSUARIO ||--o{ TAREA_EVALUABLE : valida

    %% Grupos
    TIPOUSUARIO }o--o{ GRUPO : pertenece
    GRUPO ||--o{ TAREA_GRUPAL : asigna
