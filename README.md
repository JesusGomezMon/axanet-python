# Axanet Python — Gestión de Clientes

Sistema de gestión de clientes desarrollado en Python con Programación Orientada a Objetos (POO). Permite realizar operaciones CRUD completas con persistencia en JSON y validación de datos.

## Características

- CRUD completo: crear, consultar, actualizar, eliminar y listar clientes
- Tabla hash en memoria (`dict`) para acceso O(1) por nombre de cliente
- Persistencia automática en `data/clientes.json`
- Validación de correo electrónico, teléfono de 10 dígitos y campos obligatorios
- Interfaz de consola interactiva (`python src/app.py`)
- **Interfaz web Flask** para acceso remoto desde cualquier lugar (`python src/web.py`)
- Despliegue en AWS EC2 con arranque automático (systemd)
- Suite de pruebas con pytest (24 tests)
- Pipelines CI/CD con GitHub Actions (9 workflows)
- Issue templates para solicitudes del equipo DevOps

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/JesusGomezMon/axanet-python.git
cd axanet-python

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

### Consola

```bash
python src/app.py
```

### Web (acceso remoto — EC2 o local)

```bash
python src/web.py
# Abrir http://localhost:8080
```

En AWS EC2: `http://<IP-PUBLICA>:8080`

### Menú de opciones

| Opción | Acción              |
|--------|---------------------|
| 1      | Crear cliente       |
| 2      | Consultar cliente   |
| 3      | Actualizar cliente  |
| 4      | Eliminar cliente    |
| 5      | Listar clientes     |
| 0      | Salir               |

### Ejemplo de uso programático

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path("src")))
from gestor import GestorClientes

gestor = GestorClientes("data/clientes.json")

# Crear
cliente = gestor.crear_cliente(
    nombre="Ana García",
    correo="ana@example.com",
    telefono="5512345678",
    direccion="Av. Reforma 100",
)

# Consultar
resultado = gestor.consultar_cliente("Ana García")

# Actualizar
gestor.actualizar_cliente("Ana García", telefono="5598765432")

# Listar
for c in gestor.listar_clientes():
    print(c)

# Eliminar
gestor.eliminar_cliente("Ana García")
```

## Ejecutar pruebas

```bash
pytest tests/ -v
```

## Ejecutar linter

```bash
ruff check src/ tests/
ruff format --check src/ tests/
```

## Estructura del proyecto

```
axanet-python/
│
├── src/
│   ├── cliente.py      # Clase Cliente y validaciones
│   ├── gestor.py       # GestorClientes con CRUD y tabla hash
│   ├── app.py          # Aplicación de consola
│   ├── web.py          # Servidor web Flask (EC2)
│   └── config.py       # Configuración compartida
│
├── templates/          # HTML para interfaz web
├── deploy/             # Scripts EC2, systemd, IAM
├── docs/               # Guías DevOps y guion de video
│
├── data/
│   └── clientes.json   # Persistencia de datos
│
├── tests/
│   └── test_cliente.py # Pruebas unitarias con pytest
│
├── .github/workflows/
│   ├── testing.yml             # CI: ejecutar pytest
│   ├── lint.yml                # CI: análisis con Ruff
│   ├── deploy.yml              # CD: despliegue a producción
│   ├── nuevo_cliente.yml         # Simulación: crear cliente
│   ├── cliente_actualizado.yml   # Simulación: actualizar cliente
│   ├── consulta_cliente.yml      # Simulación: consultar cliente
│   ├── mejora.yml                # Simulación: mejora/refactor
│   ├── cambio_codigo.yml         # Simulación: hotfix
│   └── nueva_funcion.yml         # Simulación: nueva funcionalidad
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Validaciones

| Campo    | Regla                                              |
|----------|----------------------------------------------------|
| Nombre   | Obligatorio, no puede estar vacío                  |
| Correo   | Obligatorio, formato válido (`usuario@dominio.com`) |
| Teléfono | Obligatorio, exactamente 10 dígitos numéricos      |
| Dirección| Opcional                                           |

## GitFlow

Este proyecto utiliza el modelo **GitFlow** para la gestión de ramas:

```
main ─────────────────────────────────────────► producción
  │
  └── develop ────────────────────────────────► integración
        │
        ├── feature/nuevo-cliente
        ├── feature/cliente-actualizado
        ├── feature/consulta-cliente
        ├── feature/nueva-funcion
        ├── feature/mejora
        │
        └── hotfix/cambio-codigo ──► merge a main y develop
```

### Ramas principales

- **`main`**: código en producción, estable y desplegable
- **`develop`**: rama de integración para nuevas funcionalidades

### Ramas de soporte

- **`feature/*`**: nuevas funcionalidades (ej. `feature/nuevo-cliente`)
- **`hotfix/*`**: correcciones urgentes en producción (ej. `hotfix/cambio-codigo`)
- **`release/*`**: preparación de versiones para producción

### Flujo de trabajo

1. Crear rama `feature/` desde `develop`
2. Desarrollar y ejecutar pruebas localmente
3. Abrir Pull Request hacia `develop`
4. CI ejecuta `testing.yml` y `lint.yml` automáticamente
5. Tras revisión, merge a `develop`
6. Cuando `develop` está listo, crear rama `release/` y merge a `main`
7. Tag de versión (`v1.0.0`) dispara `deploy.yml`

## GitHub Actions

### Workflows funcionales (CI/CD)

| Workflow      | Trigger                        | Descripción                          |
|---------------|--------------------------------|--------------------------------------|
| `testing.yml` | push/PR a `main` o `develop`   | Ejecuta pytest en cada cambio        |
| `lint.yml`    | push/PR a `main` o `develop`   | Análisis estático con Ruff           |
| `deploy.yml`  | push a `main` o tag `v*.*.*`   | Pruebas + artefacto de despliegue    |

### Workflows de simulación (GitFlow)

Estos workflows se ejecutan manualmente (`workflow_dispatch`) para simular escenarios de desarrollo:

| Workflow                  | Rama simulada                  | Propósito                        |
|---------------------------|--------------------------------|----------------------------------|
| `nuevo_cliente.yml`       | `feature/nuevo-cliente`        | Simular creación de cliente      |
| `cliente_actualizado.yml` | `feature/cliente-actualizado`| Simular actualización            |
| `consulta_cliente.yml`    | `feature/consulta-cliente`     | Simular consulta                 |
| `mejora.yml`              | `feature/mejora`               | Simular refactor/optimización    |
| `cambio_codigo.yml`       | `hotfix/cambio-codigo`         | Simular corrección urgente       |
| `nueva_funcion.yml`       | `feature/nueva-funcion`        | Simular nueva funcionalidad      |

Para ejecutar un workflow de simulación:

1. Ir a **Actions** en GitHub
2. Seleccionar el workflow deseado
3. Clic en **Run workflow**
4. Completar los parámetros y ejecutar

## Arquitectura

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   app.py    │────►│  GestorClientes  │────►│ clientes.json   │
│  (Consola)  │     │  (Tabla Hash)    │     │  (Persistencia) │
└─────────────┘     └────────┬─────────┘     └─────────────────┘
                             │
                             ▼
                      ┌─────────────┐
                      │   Cliente   │
                      │ (Validación)│
                      └─────────────┘
```

La tabla hash utiliza el **nombre del cliente** (en minúsculas) como clave, permitiendo búsquedas en tiempo constante O(1). Un índice secundario por `id_cliente` complementa las consultas por identificador numérico.

## Licencia

Proyecto educativo — DevOps Fase 2.

## Documentación adicional

- [Guía completa de implementación](docs/GUIA_IMPLEMENTACION.md)
- [Equipo y roles DevOps](docs/EQUIPO_DEVOPS.md)
- [Guion para video explicativo](docs/GUION_VIDEO.md)
