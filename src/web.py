"""Servidor web Flask para acceso remoto a la gestión de clientes Axanet."""

from flask import Flask, flash, redirect, render_template, request, url_for

from config import HOST_WEB, PUERTO_WEB, RUTA_DATOS
from gestor import GestorClientes

app = Flask(
    __name__,
    template_folder=str(RUTA_DATOS.parent.parent / "templates"),
)
app.secret_key = "axanet-dev-key-cambiar-en-produccion"

gestor = GestorClientes(RUTA_DATOS)


@app.route("/")
def inicio() -> str:
    """
    Página principal con listado de clientes.

    Returns:
        HTML renderizado con la tabla de clientes.
    """
    clientes = gestor.listar_clientes()
    return render_template("index.html", clientes=clientes)


@app.route("/crear", methods=["GET", "POST"])
def crear() -> str:
    """
    Formulario para crear un nuevo cliente.

    Returns:
        HTML del formulario o redirección tras crear.
    """
    if request.method == "POST":
        try:
            gestor.crear_cliente(
                nombre=request.form["nombre"],
                correo=request.form["correo"],
                telefono=request.form["telefono"],
                direccion=request.form.get("direccion", ""),
            )
            flash("Cliente creado exitosamente.", "success")
            return redirect(url_for("inicio"))
        except ValueError as error:
            flash(str(error), "error")

    return render_template("formulario.html", accion="crear", cliente=None)


@app.route("/consultar")
def consultar() -> str:
    """
    Consulta un cliente por nombre o ID.

    Returns:
        HTML con el resultado de la búsqueda.
    """
    identificador = request.args.get("q", "").strip()
    cliente = gestor.consultar_cliente(identificador) if identificador else None
    return render_template(
        "consultar.html", cliente=cliente, identificador=identificador
    )


@app.route("/editar/<identificador>", methods=["GET", "POST"])
def editar(identificador: str) -> str:
    """
    Formulario para actualizar un cliente existente.

    Args:
        identificador: Nombre o ID del cliente.

    Returns:
        HTML del formulario o redirección tras actualizar.
    """
    cliente = gestor.consultar_cliente(identificador)
    if cliente is None:
        flash(f"No se encontró el cliente '{identificador}'.", "error")
        return redirect(url_for("inicio"))

    if request.method == "POST":
        try:
            gestor.actualizar_cliente(
                identificador,
                nombre=request.form["nombre"],
                correo=request.form["correo"],
                telefono=request.form["telefono"],
                direccion=request.form.get("direccion", ""),
            )
            flash("Cliente actualizado exitosamente.", "success")
            return redirect(url_for("inicio"))
        except ValueError as error:
            flash(str(error), "error")

    return render_template("formulario.html", accion="editar", cliente=cliente)


@app.route("/eliminar/<identificador>", methods=["POST"])
def eliminar(identificador: str):
    """
    Elimina un cliente del sistema.

    Args:
        identificador: Nombre o ID del cliente.

    Returns:
        Redirección al listado principal.
    """
    try:
        eliminado = gestor.eliminar_cliente(identificador)
        flash(f"Cliente '{eliminado.nombre}' eliminado.", "success")
    except ValueError as error:
        flash(str(error), "error")
    return redirect(url_for("inicio"))


@app.route("/health")
def health() -> dict:
    """
    Endpoint de salud para verificación en EC2 y load balancers.

    Returns:
        JSON con estado del servicio.
    """
    return {
        "status": "ok",
        "clientes": gestor.cantidad_clientes(),
        "version": "1.0.0",
    }


def main() -> None:
    """Inicia el servidor web en todas las interfaces de red."""
    print(f"Axanet Web en http://{HOST_WEB}:{PUERTO_WEB}")
    app.run(host=HOST_WEB, port=PUERTO_WEB, debug=False)


if __name__ == "__main__":
    main()
