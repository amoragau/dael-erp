-- Insertar estados de orden de compra
INSERT INTO estados_orden_compra (codigo_estado, nombre_estado, descripcion, es_estado_inicial, es_estado_final, permite_edicion, permite_cancelacion, activo)
VALUES
    ('CREADA', 'Creada', 'Orden de compra creada', true, false, true, true, true),
    ('APROBADA', 'Aprobada', 'Orden de compra aprobada', false, false, false, true, true),
    ('ENVIADA', 'Enviada', 'Orden de compra enviada al proveedor', false, false, false, true, true),
    ('RECIBIDA', 'Recibida', 'Orden de compra recibida', false, false, false, false, true),
    ('CERRADA', 'Cerrada', 'Orden de compra cerrada', false, true, false, false, true),
    ('CANCELADA', 'Cancelada', 'Orden de compra cancelada', false, true, false, false, true)
ON CONFLICT (codigo_estado) DO NOTHING;
