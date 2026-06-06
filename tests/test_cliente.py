"""Tests unitarios para el módulo de gestión de clientes Axanet."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cliente import Cliente
from gestor import GestorClientes


@pytest.fixture
def ruta_temporal(tmp_path: Path) -> Path:
    """
    Crea un archivo JSON temporal para pruebas.

    Args:
        tmp_path: Directorio temporal proporcionado por pytest.

    Returns:
        Ruta al archivo clientes.json temporal.
    """
    archivo = tmp_path / "clientes.json"
    archivo.write_text('{"clientes": []}', encoding="utf-8")
    return archivo


@pytest.fixture
def gestor(ruta_temporal: Path) -> GestorClientes:
    """
    Proporciona una instancia de GestorClientes con datos temporales.

    Args:
        ruta_temporal: Ruta al archivo JSON de prueba.

    Returns:
        Instancia configurada de GestorClientes.
    """
    return GestorClientes(ruta_temporal)


class TestCliente:
    """Pruebas para la clase Cliente."""

    def test_crear_cliente_valido(self) -> None:
        """Verifica la creación de un cliente con datos válidos."""
        cliente = Cliente(
            id_cliente=1,
            nombre="Juan Pérez",
            correo="juan@example.com",
            telefono="5512345678",
            direccion="Calle 123",
        )
        assert cliente.nombre == "Juan Pérez"
        assert cliente.correo == "juan@example.com"
        assert cliente.telefono == "5512345678"

    def test_correo_invalido(self) -> None:
        """Verifica que un correo inválido lanza ValueError."""
        with pytest.raises(ValueError, match="Correo electrónico inválido"):
            Cliente(1, "Ana", "correo-invalido", "5512345678")

    def test_telefono_invalido_corto(self) -> None:
        """Verifica que un teléfono con menos de 10 dígitos es rechazado."""
        with pytest.raises(ValueError, match="10 dígitos"):
            Cliente(1, "Ana", "ana@example.com", "5512345")

    def test_telefono_invalido_largo(self) -> None:
        """Verifica que un teléfono con más de 10 dígitos es rechazado."""
        with pytest.raises(ValueError, match="10 dígitos"):
            Cliente(1, "Ana", "ana@example.com", "55123456789")

    def test_nombre_obligatorio(self) -> None:
        """Verifica que el nombre no puede estar vacío."""
        with pytest.raises(ValueError, match="nombre es obligatorio"):
            Cliente(1, "", "ana@example.com", "5512345678")

    def test_correo_obligatorio(self) -> None:
        """Verifica que el correo no puede estar vacío."""
        with pytest.raises(ValueError, match="correo es obligatorio"):
            Cliente(1, "Ana", "", "5512345678")

    def test_telefono_obligatorio(self) -> None:
        """Verifica que el teléfono no puede estar vacío."""
        with pytest.raises(ValueError, match="teléfono es obligatorio"):
            Cliente(1, "Ana", "ana@example.com", "")

    def test_to_dict_y_from_dict(self) -> None:
        """Verifica la serialización y deserialización del cliente."""
        original = Cliente(1, "Carlos", "carlos@example.com", "5598765432")
        datos = original.to_dict()
        restaurado = Cliente.from_dict(datos)
        assert restaurado.id_cliente == original.id_cliente
        assert restaurado.nombre == original.nombre
        assert restaurado.correo == original.correo


class TestGestorClientes:
    """Pruebas para la clase GestorClientes."""

    def test_crear_cliente(self, gestor: GestorClientes) -> None:
        """Verifica la creación de un cliente en el gestor."""
        cliente = gestor.crear_cliente(
            "María López", "maria@example.com", "5511111111", "Av. Central 45"
        )
        assert cliente.id_cliente == 1
        assert gestor.cantidad_clientes() == 1

    def test_crear_cliente_duplicado(self, gestor: GestorClientes) -> None:
        """Verifica que no se permiten nombres duplicados."""
        gestor.crear_cliente("Pedro", "pedro@example.com", "5522222222")
        with pytest.raises(ValueError, match="Ya existe un cliente"):
            gestor.crear_cliente("pedro", "otro@example.com", "5533333333")

    def test_consultar_por_nombre(self, gestor: GestorClientes) -> None:
        """Verifica la consulta de cliente por nombre."""
        gestor.crear_cliente("Laura", "laura@example.com", "5544444444")
        cliente = gestor.consultar_cliente("laura")
        assert cliente is not None
        assert cliente.nombre == "Laura"

    def test_consultar_por_id(self, gestor: GestorClientes) -> None:
        """Verifica la consulta de cliente por ID."""
        creado = gestor.crear_cliente("Diego", "diego@example.com", "5555555555")
        cliente = gestor.consultar_cliente(creado.id_cliente)
        assert cliente is not None
        assert cliente.nombre == "Diego"

    def test_consultar_inexistente(self, gestor: GestorClientes) -> None:
        """Verifica que consultar un cliente inexistente retorna None."""
        assert gestor.consultar_cliente("Inexistente") is None

    def test_actualizar_cliente(self, gestor: GestorClientes) -> None:
        """Verifica la actualización de datos de un cliente."""
        gestor.crear_cliente("Sofía", "sofia@example.com", "5566666666")
        actualizado = gestor.actualizar_cliente(
            "Sofía", correo="sofia.nueva@example.com"
        )
        assert actualizado.correo == "sofia.nueva@example.com"

    def test_actualizar_nombre(self, gestor: GestorClientes) -> None:
        """Verifica la actualización del nombre y la tabla hash."""
        gestor.crear_cliente("Roberto", "roberto@example.com", "5577777777")
        gestor.actualizar_cliente("Roberto", nombre="Roberto García")
        assert gestor.consultar_cliente("Roberto García") is not None
        assert gestor.consultar_cliente("Roberto") is None

    def test_eliminar_cliente(self, gestor: GestorClientes) -> None:
        """Verifica la eliminación de un cliente."""
        gestor.crear_cliente("Elena", "elena@example.com", "5588888888")
        eliminado = gestor.eliminar_cliente("Elena")
        assert eliminado.nombre == "Elena"
        assert gestor.cantidad_clientes() == 0

    def test_eliminar_inexistente(self, gestor: GestorClientes) -> None:
        """Verifica error al eliminar un cliente que no existe."""
        with pytest.raises(ValueError, match="No se encontró"):
            gestor.eliminar_cliente("Fantasma")

    def test_listar_clientes(self, gestor: GestorClientes) -> None:
        """Verifica el listado de múltiples clientes."""
        gestor.crear_cliente("Cliente A", "a@example.com", "5510000001")
        gestor.crear_cliente("Cliente B", "b@example.com", "5510000002")
        clientes = gestor.listar_clientes()
        assert len(clientes) == 2
        assert clientes[0].id_cliente < clientes[1].id_cliente

    def test_persistencia_json(
        self, gestor: GestorClientes, ruta_temporal: Path
    ) -> None:
        """Verifica que los datos se persisten correctamente en JSON."""
        gestor.crear_cliente("Persistente", "persist@example.com", "5599999999")

        gestor_nuevo = GestorClientes(ruta_temporal)
        cliente = gestor_nuevo.consultar_cliente("Persistente")
        assert cliente is not None
        assert cliente.correo == "persist@example.com"

        with open(ruta_temporal, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        assert len(datos["clientes"]) == 1
