"""Tests para la aplicación web Flask."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from web import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    """
    Cliente de prueba Flask con datos temporales.

    Args:
        tmp_path: Directorio temporal de pytest.
        monkeypatch: Fixture para parchear rutas.

    Returns:
        Cliente de prueba Flask.
    """
    archivo = tmp_path / "clientes.json"
    archivo.write_text('{"clientes": []}', encoding="utf-8")
    monkeypatch.setattr("web.RUTA_DATOS", archivo)
    monkeypatch.setattr("web.gestor", __import__("gestor").GestorClientes(archivo))
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestWebApp:
    """Pruebas de la interfaz web."""

    def test_inicio(self, client) -> None:
        """Verifica que la página principal responde."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Axanet" in response.data

    def test_health(self, client) -> None:
        """Verifica el endpoint de salud."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json["status"] == "ok"

    def test_crear_cliente_web(self, client) -> None:
        """Verifica creación de cliente vía formulario web."""
        response = client.post(
            "/crear",
            data={
                "nombre": "Web Test",
                "correo": "web@example.com",
                "telefono": "5512345678",
                "direccion": "Calle Web 1",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Web Test" in response.data

    def test_consultar_cliente_web(self, client) -> None:
        """Verifica consulta de cliente vía web."""
        client.post(
            "/crear",
            data={
                "nombre": "Buscar Me",
                "correo": "buscar@example.com",
                "telefono": "5598765432",
            },
        )
        response = client.get("/consultar?q=Buscar Me")
        assert response.status_code == 200
        assert b"buscar@example.com" in response.data

    def test_eliminar_cliente_web(self, client) -> None:
        """Verifica eliminación de cliente vía web."""
        client.post(
            "/crear",
            data={
                "nombre": "Eliminar Me",
                "correo": "del@example.com",
                "telefono": "5511111111",
            },
        )
        response = client.post("/eliminar/1", follow_redirects=True)
        assert response.status_code == 200
        assert b"Lista de clientes (0)" in response.data
        assert b"del@example.com" not in response.data
