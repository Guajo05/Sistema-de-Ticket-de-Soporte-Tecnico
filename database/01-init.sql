
-- =====================================================
-- SISTEMA DE TICKETS DE SOPORTE TECNICO
-- Base de datos: PostgreSQL
-- =====================================================

-- 1. Tabla de usuarios solicitantes
CREATE TABLE usuarios (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    departamento VARCHAR(100),
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de tecnicos
CREATE TABLE tecnicos (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    especialidad VARCHAR(100),
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 3. Catalogo de estados
CREATE TABLE estados_ticket (
    id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(200)
);

-- 4. Catalogo de urgencias
CREATE TABLE urgencias_ticket (
    id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(200),
    riesgo VARCHAR(20) NOT NULL,
    CONSTRAINT ck_urgencias_ticket_riesgo
        CHECK (riesgo IN ('Bajo', 'Medio', 'Alto', 'Crítico'))
);

-- 5. Tabla principal de tickets
CREATE TABLE tickets (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,

    estado_ticket_id SMALLINT NOT NULL
        REFERENCES estados_ticket(id),

    urgencia_ticket_id SMALLINT NOT NULL
        REFERENCES urgencias_ticket(id),

    usuario_id BIGINT NOT NULL
        REFERENCES usuarios(id),

    tecnico_id BIGINT
        REFERENCES tecnicos(id),

    fecha_creacion TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    fecha_actualizacion TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT ck_ticket_titulo_no_vacio
        CHECK (LENGTH(TRIM(titulo)) > 0),

    CONSTRAINT ck_ticket_descripcion_no_vacia
        CHECK (LENGTH(TRIM(descripcion)) > 0)
);

-- 1. Crear la nueva tabla de riesgos
CREATE TABLE riesgos_ticket (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(150)
);

-- 3. Agregar la nueva columna a la tabla tickets existente
ALTER TABLE tickets ADD COLUMN riesgo_ticket_id INTEGER REFERENCES riesgos_ticket(id);

-- 8. Indices para consultas y relaciones
CREATE INDEX idx_tickets_usuario
    ON tickets(usuario_id);

CREATE INDEX idx_tickets_tecnico
    ON tickets(tecnico_id);

CREATE INDEX idx_tickets_estado
    ON tickets(estado_ticket_id);

CREATE INDEX idx_tickets_urgencia
    ON tickets(urgencia_ticket_id);

CREATE INDEX idx_tickets_fecha_creacion
    ON tickets(fecha_creacion);
