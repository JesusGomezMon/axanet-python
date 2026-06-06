"""Aplicación de consola para la gestión de clientes Axanet."""

import sys

from config import RUTA_DATOS
from gestor import GestorClientes


def _mostrar_menu() -> None:
    """Muestra el menú principal de opciones."""
    print("\n" + "=" * 50)
    print("       AXANET - Gestión de Clientes")
    print("=" * 50)
    print("1. Crear cliente")
    print("2. Consultar cliente")
    print("3. Actualizar cliente")
    print("4. Eliminar cliente")
    print("5. Listar clientes")
    print("0. Salir")
    print("-" * 50)


def _leer_entrada(mensaje: str, obligatorio: bool = True) -> str:
    """
    Lee una entrada del usuario por consola.

    Args:
        mensaje: Texto a mostrar al usuario.
        obligatorio: Si True, repite hasta obtener un valor no vacío.

    Returns:
        Texto ingresado por el usuario.
    """
    while True:
        valor = input(mensaje).strip()
        if not obligatorio or valor:
            return valor
        print("Este campo es obligatorio. Intente de nuevo.")


def _mostrar_cliente(cliente) -> None:
    """
    Imprime los datos de un cliente en formato legible.

    Args:
        cliente: Instancia de Cliente a mostrar.
    """
    print("\n--- Datos del cliente ---")
    print(f"  ID:        {cliente.id_cliente}")
    print(f"  Nombre:    {cliente.nombre}")
    print(f"  Correo:    {cliente.correo}")
    print(f"  Teléfono:  {cliente.telefono}")
    print(f"  Dirección: {cliente.direccion or '(sin dirección)'}")
    print("-" * 25)


def _crear_cliente(gestor: GestorClientes) -> None:
    """
    Solicita datos y crea un nuevo cliente.

    Args:
        gestor: Instancia del gestor de clientes.
    """
    print("\n--- Crear nuevo cliente ---")
    nombre = _leer_entrada("Nombre: ")
    correo = _leer_entrada("Correo: ")
    telefono = _leer_entrada("Teléfono (10 dígitos): ")
    direccion = _leer_entrada("Dirección (opcional): ", obligatorio=False)

    try:
        cliente = gestor.crear_cliente(nombre, correo, telefono, direccion)
        print(f"\n✓ Cliente creado exitosamente con ID {cliente.id_cliente}.")
        _mostrar_cliente(cliente)
    except ValueError as error:
        print(f"\n✗ Error: {error}")


def _consultar_cliente(gestor: GestorClientes) -> None:
    """
    Busca y muestra un cliente por nombre o ID.

    Args:
        gestor: Instancia del gestor de clientes.
    """
    print("\n--- Consultar cliente ---")
    identificador = _leer_entrada("Nombre o ID del cliente: ")
    cliente = gestor.consultar_cliente(identificador)

    if cliente is None:
        print(f"\n✗ No se encontró el cliente '{identificador}'.")
    else:
        _mostrar_cliente(cliente)


def _actualizar_cliente(gestor: GestorClientes) -> None:
    """
    Actualiza los datos de un cliente existente.

    Args:
        gestor: Instancia del gestor de clientes.
    """
    print("\n--- Actualizar cliente ---")
    identificador = _leer_entrada("Nombre o ID del cliente a actualizar: ")
    cliente = gestor.consultar_cliente(identificador)

    if cliente is None:
        print(f"\n✗ No se encontró el cliente '{identificador}'.")
        return

    _mostrar_cliente(cliente)
    print("\nDeje en blanco los campos que no desea modificar.")

    nombre = _leer_entrada(f"Nuevo nombre [{cliente.nombre}]: ", obligatorio=False)
    correo = _leer_entrada(f"Nuevo correo [{cliente.correo}]: ", obligatorio=False)
    telefono = _leer_entrada(
        f"Nuevo teléfono [{cliente.telefono}]: ", obligatorio=False
    )
    direccion = _leer_entrada(
        f"Nueva dirección [{cliente.direccion}]: ", obligatorio=False
    )

    try:
        actualizado = gestor.actualizar_cliente(
            identificador,
            nombre=nombre or None,
            correo=correo or None,
            telefono=telefono or None,
            direccion=direccion or None,
        )
        print("\n✓ Cliente actualizado exitosamente.")
        _mostrar_cliente(actualizado)
    except ValueError as error:
        print(f"\n✗ Error: {error}")


def _eliminar_cliente(gestor: GestorClientes) -> None:
    """
    Elimina un cliente del sistema.

    Args:
        gestor: Instancia del gestor de clientes.
    """
    print("\n--- Eliminar cliente ---")
    identificador = _leer_entrada("Nombre o ID del cliente a eliminar: ")
    confirmacion = _leer_entrada(
        f"¿Confirma eliminar '{identificador}'? (s/n): "
    ).lower()

    if confirmacion != "s":
        print("\nOperación cancelada.")
        return

    try:
        eliminado = gestor.eliminar_cliente(identificador)
        print(f"\n✓ Cliente '{eliminado.nombre}' eliminado exitosamente.")
    except ValueError as error:
        print(f"\n✗ Error: {error}")


def _listar_clientes(gestor: GestorClientes) -> None:
    """
    Muestra todos los clientes registrados.

    Args:
        gestor: Instancia del gestor de clientes.
    """
    clientes = gestor.listar_clientes()
    print(f"\n--- Listado de clientes ({len(clientes)} total) ---")

    if not clientes:
        print("No hay clientes registrados.")
        return

    print(f"{'ID':<6}{'Nombre':<25}{'Correo':<30}{'Teléfono':<12}")
    print("-" * 73)
    for cliente in clientes:
        print(
            f"{cliente.id_cliente:<6}{cliente.nombre:<25}"
            f"{cliente.correo:<30}{cliente.telefono:<12}"
        )


def main() -> None:
    """Punto de entrada principal de la aplicación de consola."""
    gestor = GestorClientes(RUTA_DATOS)
    print("\nBienvenido al sistema de gestión de clientes Axanet.")

    acciones = {
        "1": _crear_cliente,
        "2": _consultar_cliente,
        "3": _actualizar_cliente,
        "4": _eliminar_cliente,
        "5": _listar_clientes,
    }

    while True:
        _mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            print("\n¡Hasta pronto!")
            sys.exit(0)

        accion = acciones.get(opcion)
        if accion is None:
            print("\n✗ Opción no válida. Intente de nuevo.")
            continue

        accion(gestor)


if __name__ == "__main__":
    main()
