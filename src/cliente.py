"""Módulo que define la entidad Cliente y sus validaciones."""

import re
from typing import Any


class Cliente:
    """
    Representa un cliente del sistema Axanet.

    Attributes:
        id_cliente (int): Identificador único del cliente.
        nombre (str): Nombre completo del cliente.
        correo (str): Correo electrónico del cliente.
        telefono (str): Número telefónico de 10 dígitos.
        direccion (str): Dirección física del cliente.
    """

    PATRON_CORREO = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    PATRON_TELEFONO = re.compile(r"^\d{10}$")

    def __init__(
        self,
        id_cliente: int,
        nombre: str,
        correo: str,
        telefono: str,
        direccion: str = "",
    ) -> None:
        """
        Inicializa una instancia de Cliente con validación de campos.

        Args:
            id_cliente: Identificador único del cliente.
            nombre: Nombre completo del cliente.
            correo: Correo electrónico válido.
            telefono: Teléfono de exactamente 10 dígitos.
            direccion: Dirección del cliente (opcional).

        Raises:
            ValueError: Si algún campo obligatorio es inválido.
        """
        self.id_cliente = id_cliente
        self.nombre = nombre.strip()
        self.correo = correo.strip()
        self.telefono = telefono.strip()
        self.direccion = direccion.strip()
        self._validar()

    def _validar(self) -> None:
        """
        Valida los campos obligatorios y el formato de correo y teléfono.

        Raises:
            ValueError: Si algún campo no cumple las reglas de validación.
        """
        if not self.nombre:
            raise ValueError("El nombre es obligatorio.")
        if not self.correo:
            raise ValueError("El correo es obligatorio.")
        if not self.PATRON_CORREO.match(self.correo):
            raise ValueError(f"Correo electrónico inválido: {self.correo}")
        if not self.telefono:
            raise ValueError("El teléfono es obligatorio.")
        if not self.PATRON_TELEFONO.match(self.telefono):
            raise ValueError(
                f"El teléfono debe contener exactamente 10 dígitos: {self.telefono}"
            )

    def to_dict(self) -> dict[str, Any]:
        """
        Convierte el cliente a un diccionario serializable.

        Returns:
            Diccionario con los atributos del cliente.
        """
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "correo": self.correo,
            "telefono": self.telefono,
            "direccion": self.direccion,
        }

    @classmethod
    def from_dict(cls, datos: dict[str, Any]) -> "Cliente":
        """
        Crea una instancia de Cliente a partir de un diccionario.

        Args:
            datos: Diccionario con los datos del cliente.

        Returns:
            Instancia de Cliente validada.
        """
        return cls(
            id_cliente=int(datos["id_cliente"]),
            nombre=str(datos["nombre"]),
            correo=str(datos["correo"]),
            telefono=str(datos["telefono"]),
            direccion=str(datos.get("direccion", "")),
        )

    def __str__(self) -> str:
        """Retorna una representación legible del cliente."""
        return (
            f"Cliente(id={self.id_cliente}, nombre='{self.nombre}', "
            f"correo='{self.correo}', telefono='{self.telefono}', "
            f"direccion='{self.direccion}')"
        )

    def __repr__(self) -> str:
        """Retorna una representación técnica del cliente."""
        return self.__str__()
