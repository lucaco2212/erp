# Sistema académico de cuentas contables

Aplicación web simple enfocada exclusivamente en representar cuentas contables, clasificarlas y validar asientos con reglas básicas de Debe y Haber.

## Ejecutar

```bash
python3 app.py
```

Luego abrir `http://127.0.0.1:8000`.

## Base de datos

La aplicación usa SQLite. La tabla `CuentaContable` se crea desde `schema.sql` con los campos mínimos requeridos:

- `id`
- `codigo`
- `nombre`
- `tipo_cuenta`
- `clasificacion`
- `corriente_no_corriente`
- `saldo`

## Pruebas

```bash
python3 -m unittest
```
