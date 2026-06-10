import sqlite3
import tempfile
import unittest
from pathlib import Path

from database import initialize_database, list_accounts


class CuentaContableDatabaseTest(unittest.TestCase):
    def test_schema_and_seed_accounts_match_required_catalog(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "test.db"
            initialize_database(db_path)
            accounts = list_accounts(db_path)

            self.assertEqual(len(accounts), 12)
            self.assertIn("Caja", {account["nombre"] for account in accounts})
            self.assertIn("Capital", {account["nombre"] for account in accounts})

            with sqlite3.connect(db_path) as connection:
                columns = [row[1] for row in connection.execute("PRAGMA table_info(CuentaContable)")]

            self.assertEqual(
                columns,
                [
                    "id",
                    "codigo",
                    "nombre",
                    "tipo_cuenta",
                    "clasificacion",
                    "corriente_no_corriente",
                    "saldo",
                ],
            )

    def test_required_accounts_are_classified_by_type_and_current_status(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "test.db"
            initialize_database(db_path)
            accounts = {account["nombre"]: account for account in list_accounts(db_path)}

            expected = {
                "Caja": ("Activo", "Corriente"),
                "Vehículos": ("Activo", "No corriente"),
                "Banco": ("Activo", "Corriente"),
                "Edificios": ("Activo", "No corriente"),
                "Equipos computacionales": ("Activo", "No corriente"),
                "Cuentas por cobrar a clientes menor a 1 año": ("Activo", "Corriente"),
                "Ventas en cuotas a más de 12 meses": ("Activo", "No corriente"),
                "Créditos Hipotecarios": ("Pasivo", "No corriente"),
                "Proveedores": ("Pasivo", "Corriente"),
                "Cuentas por pagar corto plazo": ("Pasivo", "Corriente"),
                "Deudas bancarias con vencimiento menor a 1 año": ("Pasivo", "Corriente"),
                "Capital": ("Patrimonio", "No aplica"),
            }

            self.assertEqual(set(accounts), set(expected))
            for name, (account_type, current_status) in expected.items():
                self.assertEqual(accounts[name]["tipo_cuenta"], account_type)
                self.assertEqual(accounts[name]["corriente_no_corriente"], current_status)


if __name__ == "__main__":
    unittest.main()
