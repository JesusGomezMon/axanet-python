"""Configuración compartida de rutas y constantes del proyecto."""

from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_DATOS = RAIZ_PROYECTO / "data" / "clientes.json"
PUERTO_WEB = 8080
HOST_WEB = "0.0.0.0"
