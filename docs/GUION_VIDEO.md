# Guion para video explicativo — Axanet Python DevOps

**Duración estimada:** 12 minutos  
**Herramienta sugerida:** OBS Studio, Loom, o Win+G (Xbox Game Bar)

---

## Introducción (0:00 - 1:00)

> "Hola, soy [tu nombre]. En este video explico cómo implementé el proyecto Axanet Python siguiendo metodología DevOps: GitHub colaborativo, GitHub Actions, versionado y despliegue en AWS EC2."

Mostrar:
- Repositorio en GitHub
- Estructura de carpetas del proyecto

---

## 1. Proyecto colaborativo GitHub (1:00 - 2:30)

Mostrar:
- URL del repositorio
- **Settings → Collaborators** con miembros del equipo
- Tabla de roles (desarrolladores, TI, atención al cliente)
- Ramas: `main`, `develop`, `feature/*`

Decir:
> "Cada miembro tiene un rol según DevOps: los desarrolladores revisan código, TI gestiona infraestructura, y atención al cliente crea issues de operación."

---

## 2. Aplicación Python (2:30 - 4:00)

Demostrar en terminal:
```bash
python src/app.py
```
- Crear un cliente
- Consultar, modificar, eliminar

Luego mostrar la versión web:
```bash
python src/web.py
```
- Abrir `http://localhost:8080`
- Realizar las mismas operaciones en el navegador

Decir:
> "La versión web permite acceso desde cualquier lugar, no solo desde consola."

---

## 3. GitHub Actions (4:00 - 6:00)

Mostrar:
- Pestaña **Actions** con workflows ejecutados
- Crear un **Issue** usando template "Nuevo Cliente"
- Mostrar cómo el workflow se activa automáticamente
- Mostrar el comentario automático del bot en el issue

Repetir brevemente con issue de "Mejora" o "Nueva función".

Decir:
> "Cada tipo de solicitud del equipo dispara su propio pipeline de validación."

---

## 4. Despliegue AWS EC2 (6:00 - 8:30)

Mostrar en consola AWS:
- Usuarios IAM creados (6 usuarios, 3 categorías)
- Instancia EC2 t2.micro Amazon Linux 2, 8 GiB
- Security Group con puerto 8080 abierto
- Servicio systemd `axanet` corriendo

En terminal SSH:
```bash
sudo systemctl status axanet
curl http://localhost:8080/health
```

Decir:
> "La aplicación arranca automáticamente al encender la instancia gracias a systemd."

---

## 5. Acceso desde cualquier lugar (8:30 - 9:30)

**Parte clave del video:**

1. Desde tu celular (datos móviles, NO WiFi de casa) abrir:
   `http://<IP-PUBLICA-EC2>:8080`
2. Crear un cliente desde el teléfono
3. Opcional: pedir a un compañero que acceda desde su casa/escuela

Decir:
> "Cualquier miembro del equipo puede gestionar clientes desde casa, escuela, oficina o un café, porque la app está en la nube."

---

## 6. Versionado y rollback (9:30 - 11:30)

Mostrar:
- **GitHub Releases** con v1.0.0 y v1.1.0
- Rama con código roto (demo de falla)

Demostrar rollback:
```bash
git checkout v1.0.0
sudo systemctl restart axanet
```

Verificar que la app funciona de nuevo:
- `http://<IP>:8080/health` → status ok
- Crear cliente exitosamente

Decir:
> "Cuando una versión falla, GitHub nos permite volver a una versión anterior en segundos y mantener el servicio en línea."

---

## Cierre (11:30 - 12:00)

Resumir:
1. GitHub colaborativo con roles DevOps
2. App Python con CRUD completo
3. 6 workflows de GitHub Actions
4. Despliegue en AWS EC2 con IAM
5. Acceso global vía web
6. Versionado y rollback

> "Gracias por ver el video. El código está en github.com/JesusGomezMon/axanet-python"

---

## Tips de grabación

- Usa resolución 1920x1080
- Graba la pantalla completa al cambiar entre GitHub, terminal y AWS
- Habla despacio al mostrar URLs y comandos
- Pausa 2 segundos después de cada acción para que se vea el resultado
