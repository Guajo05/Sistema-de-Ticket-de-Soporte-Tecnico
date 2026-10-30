-- =====================================================
-- DATOS INICIALES DE CATALOGOS
-- Se puede ejecutar varias veces sin duplicar datos
-- =====================================================

INSERT INTO estados_ticket (nombre, descripcion) VALUES
    ('Abierto',     'Ticket recién creado, pendiente de atención'),
    ('En progreso', 'Un técnico está trabajando en el ticket'),
    ('Resuelto',    'El problema fue solucionado, pendiente de confirmación'),
    ('Cerrado',     'Ticket finalizado')
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO urgencias_ticket (nombre, descripcion, riesgo) VALUES
    ('Baja',    'No afecta el trabajo diario',        'Bajo'),
    ('Media',   'Afecta parcialmente el trabajo',     'Medio'),
    ('Alta',    'Afecta seriamente el trabajo',       'Alto'),
    ('Crítica', 'Bloquea por completo la operación', 'Crítico')
ON CONFLICT (nombre) DO NOTHING;

-- 2. Insertar algunos datos de prueba
INSERT INTO riesgos_ticket (nombre, descripcion) VALUES 
('Bajo', 'No afecta la operatividad'),
('Medio', 'Afecta a un departamento'),
('Alto', 'Compromete datos o seguridad');
