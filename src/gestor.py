"""Módulo de gestión CRUD de clientes con persistencia en JSON."""

import json
from pathlib import Path
from typing import Optional

from cliente import Cliente


class GestorClientes:
    """
    Gestiona operaciones CRUD sobre clientes usando un diccionario como tabla hash.

    La tabla hash utiliza el nombre del cliente como clave para acceso O(1).

    Attributes:
        ruta_datos (Path): Ruta al archivo JSON de persistencia.
        _tabla_hash (dict[str, Cliente]): Tabla hash nombre -> Cliente.
        _indice_ids (dict[int, str]): Índice id_cliente -> nombre.
        _siguiente_id (int): Próximo identificador disponible.
    """

    def __init__(self, ruta_datos: str | Path) -> None:
        """
        Inicializa el gestor y carga los clientes desde el archivo JSON.

        Args:
            ruta_datos: Ruta al archivo clientes.json.
        """
        self.ruta_datos = Path(ruta_datos)
        self._tabla_hash: dict[str, Cliente] = {}
        self._indice_ids: dict[int, str] = {}
        self._siguiente_id: int = 1
        self._cargar_datos()

    def _cargar_datos(self) -> None:
        """
        Carga clientes desde el archivo JSON y reconstruye la tabla hash.

        Si el archivo no existe, se inicializa con una estructura vacía.
        """
        self.ruta_datos.parent.mkdir(parents=True, exist_ok=True)

        if not self.ruta_datos.exists():
            self._guardar_datos()
            return

        with open(self.ruta_datos, "r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)

        clientes_data = contenido.get("clientes", [])
        self._tabla_hash.clear()
        self._indice_ids.clear()
        max_id = 0

        for datos in clientes_data:
            cliente = Cliente.from_dict(datos)
            self._tabla_hash[cliente.nombre.lower()] = cliente
            self._indice_ids[cliente.id_cliente] = cliente.nombre.lower()
            max_id = max(max_id, cliente.id_cliente)

        self._siguiente_id = max_id + 1 if max_id > 0 else 1

    def _guardar_datos(self) -> None:
        """Persiste todos los clientes en el archivo JSON."""
        clientes_ordenados = sorted(
            self._tabla_hash.values(), key=lambda c: c.id_cliente
        )
        contenido = {"clientes": [cliente.to_dict() for cliente in clientes_ordenados]}
        with open(self.ruta_datos, "w", encoding="utf-8") as archivo:
            json.dump(contenido, archivo, indent=2, ensure_ascii=False)

    def crear_cliente(
        self,
        nombre: str,
        correo: str,
        telefono: str,
        direccion: str = "",
    ) -> Cliente:
        """
        Crea un nuevo cliente y lo almacena en la tabla hash.

        Args:
            nombre: Nombre del cliente.
            correo: Correo electrónico válido.
            telefono: Teléfono de 10 dígitos.
            direccion: Dirección del cliente.

        Returns:
            Instancia del cliente creado.

        Raises:
            ValueError: Si el nombre ya existe o los datos son inválidos.
        """
        clave = nombre.strip().lower()
        if clave in self._tabla_hash:
            raise ValueError(f"Ya existe un cliente con el nombre '{nombre}'.")

        cliente = Cliente(
            id_cliente=self._siguiente_id,
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            direccion=direccion,
        )
        self._tabla_hash[clave] = cliente
        self._indice_ids[cliente.id_cliente] = clave
        self._siguiente_id += 1
        self._guardar_datos()
        return cliente

    def consultar_cliente(self, identificador: str | int) -> Optional[Cliente]:
        """
        Consulta un cliente por nombre o id_cliente.

        Args:
            identificador: Nombre del cliente o id numérico.

        Returns:
            Cliente encontrado o None si no existe.
        """
        if isinstance(identificador, int) or str(identificador).isdigit():
            id_cliente = int(identificador)
            clave = self._indice_ids.get(id_cliente)
            if clave is None:
                return None
            return self._tabla_hash.get(clave)

        clave = str(identificador).strip().lower()
        return self._tabla_hash.get(clave)

    def actualizar_cliente(
        self,
        identificador: str | int,
        nombre: Optional[str] = None,
        correo: Optional[str] = None,
        telefono: Optional[str] = None,
        direccion: Optional[str] = None,
    ) -> Cliente:
        """
        Actualiza los datos de un cliente existente.

        Args:
            identificador: Nombre o id del cliente a actualizar.
            nombre: Nuevo nombre (opcional).
            correo: Nuevo correo (opcional).
            telefono: Nuevo teléfono (opcional).
            direccion: Nueva dirección (opcional).

        Returns:
            Cliente actualizado.

        Raises:
            ValueError: Si el cliente no existe o el nuevo nombre ya está en uso.
        """
        cliente = self.consultar_cliente(identificador)
        if cliente is None:
            raise ValueError(f"No se encontró el cliente: {identificador}")

        clave_actual = cliente.nombre.lower()
        nuevo_nombre = nombre.strip() if nombre is not None else cliente.nombre
        nuevo_correo = correo.strip() if correo is not None else cliente.correo
        nuevo_telefono = telefono.strip() if telefono is not None else cliente.telefono
        nueva_direccion = (
            direccion.strip() if direccion is not None else cliente.direccion
        )

        nueva_clave = nuevo_nombre.lower()
        if nueva_clave != clave_actual and nueva_clave in self._tabla_hash:
            raise ValueError(f"Ya existe un cliente con el nombre '{nuevo_nombre}'.")

        cliente_actualizado = Cliente(
            id_cliente=cliente.id_cliente,
            nombre=nuevo_nombre,
            correo=nuevo_correo,
            telefono=nuevo_telefono,
            direccion=nueva_direccion,
        )

        if nueva_clave != clave_actual:
            del self._tabla_hash[clave_actual]

        self._tabla_hash[nueva_clave] = cliente_actualizado
        self._indice_ids[cliente_actualizado.id_cliente] = nueva_clave
        self._guardar_datos()
        return cliente_actualizado

    def eliminar_cliente(self, identificador: str | int) -> Cliente:
        """
        Elimina un cliente de la tabla hash y del archivo JSON.

        Args:
            identificador: Nombre o id del cliente a eliminar.

        Returns:
            Cliente eliminado.

        Raises:
            ValueError: Si el cliente no existe.
        """
        cliente = self.consultar_cliente(identificador)
        if cliente is None:
            raise ValueError(f"No se encontró el cliente: {identificador}")

        clave = cliente.nombre.lower()
        del self._tabla_hash[clave]
        del self._indice_ids[cliente.id_cliente]
        self._guardar_datos()
        return cliente

    def listar_clientes(self) -> list[Cliente]:
        """
        Retorna la lista de todos los clientes ordenados por id.

        Returns:
            Lista de instancias Cliente.
        """
        return sorted(self._tabla_hash.values(), key=lambda c: c.id_cliente)

    def cantidad_clientes(self) -> int:
        """
        Retorna el número total de clientes registrados.

        Returns:
            Cantidad de clientes en la tabla hash.
        """
        return len(self._tabla_hash)
