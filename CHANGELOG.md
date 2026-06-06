# Changelog

## [1.1.0] - Versión con interfaz web (develop)

### Added
- Interfaz web Flask accesible desde cualquier lugar (`src/web.py`)
- Templates HTML para CRUD visual
- Endpoint `/health` para monitoreo en EC2
- Scripts de despliegue AWS EC2 (`deploy/`)
- Políticas IAM para desarrolladores, TI y atención al cliente
- Issue templates para solicitudes del equipo
- Workflows GitHub Actions activados por issues

## [1.0.0] - Versión estable inicial (main)

### Added
- Clase `Cliente` con validaciones
- `GestorClientes` con CRUD y tabla hash
- Aplicación de consola (`src/app.py`)
- Persistencia en `data/clientes.json`
- 19 pruebas unitarias con pytest
- Workflows CI/CD: testing, lint, deploy
