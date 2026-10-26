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

INSERT INTO urgencias_ticket (nombre, descripcion) VALUES
    ('Baja',    'No afecta el trabajo diario'),
    ('Media',   'Afecta parcialmente el trabajo'),
    ('Alta',    'Afecta seriamente el trabajo'),
    ('Crítica', 'Bloquea por completo la operación')
ON CONFLICT (nombre) DO NOTHING;
