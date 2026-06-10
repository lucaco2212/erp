-- Estructura mínima solicitada para registrar una cuenta contable.
CREATE TABLE IF NOT EXISTS CuentaContable (
    id INTEGER PRIMARY KEY,
    codigo TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    tipo_cuenta TEXT NOT NULL CHECK (tipo_cuenta IN ('Activo', 'Pasivo', 'Patrimonio')),
    clasificacion TEXT NOT NULL,
    corriente_no_corriente TEXT NOT NULL CHECK (corriente_no_corriente IN ('Corriente', 'No corriente', 'No aplica')),
    saldo REAL NOT NULL DEFAULT 0
);
