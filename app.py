"""Servidor HTTP mínimo para el sistema académico de contabilidad."""
from __future__ import annotations

import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from database import initialize_database, list_accounts

ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "static"


class AccountingHandler(SimpleHTTPRequestHandler):
    """Sirve la interfaz estática y una API pequeña para cuentas contables."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self) -> None:  # noqa: N802 - nombre definido por http.server
        path = urlparse(self.path).path
        if path == "/api/cuentas":
            self._send_json(list_accounts())
            return
        if path == "/":
            self.path = "/index.html"
        super().do_GET()

    def _send_json(self, payload: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Inicializa SQLite y levanta el servidor local de aprendizaje."""
    initialize_database()
    server = ThreadingHTTPServer((host, port), AccountingHandler)
    print(f"Aplicación disponible en http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
