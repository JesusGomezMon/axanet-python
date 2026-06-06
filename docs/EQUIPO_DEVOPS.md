# Equipo DevOps — Axanet Python

## Composición del equipo (6 miembros)

| # | Rol | Categoría | GitHub Role | AWS IAM |
|---|-----|-----------|-------------|---------|
| 1 | Desarrollador Senior | Desarrollo | Maintain | axanet-dev1 |
| 2 | Desarrollador Junior | Desarrollo | Write | axanet-dev2 |
| 3 | Admin de Sistemas | TI | Maintain | axanet-ti1 |
| 4 | Soporte Técnico | TI | Write | axanet-ti2 |
| 5 | Agente Atención | Atención | Triage | axanet-atencion1 |
| 6 | Agente Atención | Atención | Triage | axanet-atencion2 |

## Responsabilidades por categoría

### Desarrolladores (2)
- Escribir y revisar código Python
- Crear Pull Requests hacia `develop`
- Ejecutar pruebas locales (`pytest`)
- Aprobar merges de features

### TI (2)
- Gestionar instancia EC2 y Security Groups
- Configurar usuarios IAM en AWS
- Monitorear workflows de GitHub Actions
- Ejecutar despliegues a producción (`main`)

### Atención al cliente (2)
- Crear issues para operaciones CRUD de clientes
- Consultar información via interfaz web
- Reportar bugs via issue template "Cambio de código"
- Solicitar mejoras via issue template "Mejora"

## Flujo de trabajo típico

```
Atención crea Issue → GitHub Action valida → Dev implementa → PR → Review → Merge → Deploy EC2
```

## Invitar miembros

Reemplaza los usuarios de ejemplo con los GitHub usernames reales de tu equipo:

```
Settings → Collaborators → Add people
```

Para equipos organizacionales:
```
Settings → Teams → Create team → Add members
```
