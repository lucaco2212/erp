"""Persistencia SQLite para la aplicación académica de cuentas contables."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "contabilidad_academica.db"
SCHEMA_PATH = ROOT / "schema.sql"

# Catálogo académico requerido por el enunciado. Los códigos son simples para
# facilitar la lectura y mantener el foco en la clasificación contable.
SEED_ACCOUNTS = [
    (1, "1.1.01", "Caja", "Activo", "Disponible", "Corriente", 0),
    (2, "1.2.01", "Vehículos", "Activo", "Propiedad, planta y equipo", "No corriente", 0),
    (3, "1.1.02", "Banco", "Activo", "Disponible", "Corriente", 0),
    (4, "1.2.02", "Edificios", "Activo", "Propiedad, planta y equipo", "No corriente", 0),
    (5, "1.2.03", "Equipos computacionales", "Activo", "Propiedad, planta y equipo", "No corriente", 0),
    (6, "1.1.03", "Cuentas por cobrar a clientes menor a 1 año", "Activo", "Cuentas por cobrar", "Corriente", 0),
    (7, "1.2.04", "Ventas en cuotas a más de 12 meses", "Activo", "Cuentas por cobrar de largo plazo", "No corriente", 0),
    (8, "2.2.01", "Créditos Hipotecarios", "Pasivo", "Obligaciones financieras", "No corriente", 0),
    (9, "2.1.01", "Proveedores", "Pasivo", "Cuentas por pagar", "Corriente", 0),
    (10, "2.1.02", "Cuentas por pagar corto plazo", "Pasivo", "Cuentas por pagar", "Corriente", 0),
    (11, "2.1.03", "Deudas bancarias con vencimiento menor a 1 año", "Pasivo", "Obligaciones financieras", "Corriente", 0),
    (12, "3.0.01", "Capital", "Patrimonio", "Capital social", "No aplica", 0),
]


def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Abre una conexión SQLite con filas accesibles por nombre de columna."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: Path = DB_PATH) -> None:
    """Crea la tabla CuentaContable e inserta las cuentas solicitadas."""
    with connect(db_path) as connection:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        connection.executemany(
            """
            INSERT OR IGNORE INTO CuentaContable
                (id, codigo, nombre, tipo_cuenta, clasificacion, corriente_no_corriente, saldo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            SEED_ACCOUNTS,
        )
        connection.commit()


def list_accounts(db_path: Path = DB_PATH) -> list[dict]:
    """Devuelve todas las cuentas ordenadas para mostrarlas agrupadas en la UI."""
    initialize_database(db_path)
    with connect(db_path) as connection:
        rows: Iterable[sqlite3.Row] = connection.execute(
            """
            SELECT id, codigo, nombre, tipo_cuenta, clasificacion, corriente_no_corriente, saldo
            FROM CuentaContable
            ORDER BY tipo_cuenta, corriente_no_corriente, codigo
            """
        )
        return [dict(row) for row in rows]


if __name__ == "__main__":
    initialize_database()
    print(f"Base de datos inicializada en {DB_PATH}")
