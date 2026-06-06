# Guía completa de implementación — Axanet Python

Esta guía cubre **todas las indicaciones** del proyecto DevOps paso a paso.

---

## 1. Proyecto colaborativo en GitHub

### Repositorio
- URL: `https://github.com/JesusGomezMon/axanet-python`
- Visibilidad: Público (cuenta gratuita)

### Roles del equipo (metodología DevOps)

| Rol GitHub | Usuario ejemplo | Responsabilidad |
|------------|-----------------|-----------------|
| **Admin** | Líder del proyecto | Configuración, despliegue, merges a `main` |
| **Maintain** | Dev 1, Dev 2 | Revisión de PR, merge a `develop` |
| **Write** | TI 1, TI 2 | Infraestructura, workflows, EC2 |
| **Triage** | Atención 1, Atención 2 | Crear issues de clientes |
| **Read** | Observadores | Solo lectura |

### Agregar miembros al equipo

1. Ve a **Settings → Collaborators** (o **Manage access**)
2. Clic en **Add people**
3. Ingresa el usuario de GitHub de cada miembro
4. Asigna el rol según la tabla anterior

### Estructura de ramas (GitFlow)

```
main        → producción (v1.0.0 estable)
develop     → integración (v1.1.0 con web)
feature/*   → nuevas funciones
hotfix/*    → correcciones urgentes
```

---

## 2. Aplicación Python — Gestión de clientes

### Ejecución local

```bash
# Consola
python src/app.py

# Web (acceso remoto)
python src/web.py
# Abrir: http://localhost:8080
```

### CRUD disponible
- Crear, consultar, actualizar, eliminar y listar clientes
- Validación de correo, teléfono 10 dígitos, campos obligatorios
- Tabla hash en memoria + persistencia JSON

---

## 3. GitHub Actions — Flujos de solicitudes

| Solicitud | Issue template | Workflow | Label |
|-----------|---------------|----------|-------|
| Nuevo cliente | `nuevo-cliente.yml` | `nuevo_cliente.yml` | `nuevo-cliente` |
| Modificar cliente | `modificar-cliente.yml` | `cliente_actualizado.yml` | `cliente-actualizado` |
| Consultar cliente | `consulta-cliente.yml` | `consulta_cliente.yml` | `consulta-cliente` |
| Mejora | `mejora.yml` | `mejora.yml` | `mejora` |
| Cambio de código | `cambio-codigo.yml` | `cambio_codigo.yml` | `cambio-codigo` |
| Nueva función | `nueva-funcion.yml` | `nueva_funcion.yml` | `nueva-funcion` |

### Probar un workflow
1. **Issues → New issue** → selecciona el template
2. Completa el formulario y envía
3. Ve a **Actions** y verifica que el workflow se ejecutó
4. El bot comentará en el issue con el resultado

---

## 4. Despliegue en AWS EC2

### 4.1 Crear cuenta AWS (Free Tier)
1. Registrarse en [aws.amazon.com](https://aws.amazon.com)
2. Activar Free Tier (12 meses)

### 4.2 Crear usuarios IAM (6 usuarios)

En **IAM → Users → Create user**:

| Usuario | Grupo | Política |
|---------|-------|----------|
| `axanet-dev1` | Desarrolladores | `deploy/iam/policy-desarrollador.json` |
| `axanet-dev2` | Desarrolladores | `deploy/iam/policy-desarrollador.json` |
| `axanet-ti1` | TI | `deploy/iam/policy-ti.json` |
| `axanet-ti2` | TI | `deploy/iam/policy-ti.json` |
| `axanet-atencion1` | Atencion | `deploy/iam/policy-atencion-cliente.json` |
| `axanet-atencion2` | Atencion | `deploy/iam/policy-atencion-cliente.json` |

### 4.3 Lanzar instancia EC2

1. **EC2 → Launch Instance**
2. Configuración:
   - **Nombre:** axanet-python-prod
   - **AMI:** Amazon Linux 2
   - **Tipo:** t2.micro (Free Tier)
   - **Almacenamiento:** 8 GiB gp2
   - **Security Group:** abrir puertos **22** (SSH) y **8080** (HTTP app)
3. **Advanced → User data:** pegar contenido de `deploy/user-data.sh`
4. Crear o seleccionar key pair para SSH
5. Launch

### 4.4 Instalación manual (alternativa)

```bash
ssh -i tu-key.pem ec2-user@<IP-PUBLICA>
curl -O https://raw.githubusercontent.com/JesusGomezMon/axanet-python/main/deploy/install.sh
chmod +x install.sh
sudo ./install.sh
```

### 4.5 Verificar despliegue

```bash
# Desde la instancia
sudo systemctl status axanet
curl http://localhost:8080/health

# Desde cualquier lugar (casa, escuela, café)
http://<IP-PUBLICA-EC2>:8080
```

---

## 5. Versionado y rollback

### Versiones

| Tag | Rama | Descripción |
|-----|------|-------------|
| `v1.0.0` | `main` | Consola estable, CRUD completo |
| `v1.1.0` | `develop` | + Interfaz web Flask |

### Guardar versiones con GitHub

```bash
git tag -a v1.0.0 -m "Versión estable consola"
git push origin v1.0.0

git tag -a v1.1.0 -m "Versión con interfaz web"
git push origin v1.1.0
```

También puedes usar **GitHub Releases**: Releases → Create new release → seleccionar tag.

### Simular falla y rollback

**Paso 1 — Romper la versión actual:**
```bash
git checkout main
# Editar src/gestor.py y borrar el método _guardar_datos
git commit -m "INTENCIONAL: romper persistencia para demo rollback"
git push
```

**Paso 2 — Verificar que falla:**
```bash
pytest tests/ -v   # Debe fallar
python src/app.py  # Error al crear cliente
```

**Paso 3 — Rollback con GitHub:**
- Opción A: `git revert HEAD` y push
- Opción B: En GitHub → **Releases → v1.0.0 → Browse files** → crear hotfix
- Opción C: `git checkout v1.0.0 -b hotfix/rollback` → merge a main

**Paso 4 — Redesplegar en EC2:**
```bash
ssh ec2-user@<IP>
cd /opt/axanet-python
git fetch --tags
git checkout v1.0.0
sudo systemctl restart axanet
curl http://localhost:8080/health   # Debe responder OK
```

---

## 6. Pruebas de verificación

### Checklist

- [ ] Crear cliente (web y consola)
- [ ] Modificar cliente existente
- [ ] Consultar por nombre e ID
- [ ] Eliminar cliente
- [ ] Crear issue "Nuevo cliente" → workflow OK
- [ ] Crear issue "Mejora" → workflow OK
- [ ] Acceder desde otro dispositivo/red: `http://<IP>:8080`
- [ ] Simular falla → rollback → servicio restaurado

---

## 7. Video — Guion sugerido

Ver archivo `docs/GUION_VIDEO.md` para el guion completo minuto a minuto.

**Duración sugerida:** 10-15 minutos

**Herramientas:** OBS Studio, Loom, o grabación de pantalla de Windows (Win+G)

---

## 8. Sugerencias de mejora implementables

1. **Exportar clientes a CSV** — nueva función en `gestor.py`
2. **Autenticación básica** — proteger la web con login simple
3. **Base de datos DynamoDB** — reemplazar JSON para escalar en AWS

Estas mejoras pueden implementarse en ramas `feature/` y demostrar el flujo completo DevOps.
