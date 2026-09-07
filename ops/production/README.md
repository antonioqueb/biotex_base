# Operación técnica de producción y QA

Configuración del 6 de septiembre de 2026. Estos procedimientos sustituyen los scripts históricos de demo. No instalar `biotex_demo` ni ejecutar sus generadores en estos entornos.

## Entornos

| Concepto | Producción | QA |
|---|---|---|
| Directorio | `/opt/bioteczac/production` | `/opt/bioteczac/qa` |
| Proyecto Compose | `bioteczac-production` | `bioteczac-qa` |
| Única base de negocio del clúster | `bioteczac` | `bioteczac` |
| Origen HTTP local | `127.0.0.1:1400` | `127.0.0.1:1401` |
| Acceso público HTTPS | `https://2.24.78.58:1400/odoo` | `https://2.24.78.58:1401/odoo` |
| Workers HTTP / cron | 4 / 1 | 1 / 0 |
| Accesos de usuarios Odoo | Los vigentes en producción | Mismos usuarios, contraseñas y permisos del corte |

Cada entorno tiene PostgreSQL, archivos, sesiones, código y secretos separados. La base técnica `postgres` y las plantillas del motor no son bases adicionales de Odoo. El rol aplicativo tiene CONNECT para el arranque nativo de Odoo, sin SUPERUSER, CREATEDB, CREATEROLE ni REPLICATION. El gestor de bases está bloqueado en Nginx y Odoo.

Odoo y Nginx ejecutan con usuarios sin privilegios y sistema de archivos de solo lectura, salvo sus volúmenes y temporales. PostgreSQL y Odoo no publican puertos. Nginx conserva los orígenes HTTP en loopback y permite los listeners HTTPS públicos descritos abajo. Nginx utiliza `worker_processes auto`; la configuración de CPU, RAM y concurrencia corresponde al servidor actual de 4 CPU y 16 GB, y debe medirse antes de aumentar workers. El código Enterprise está en `/opt/bioteczac/enterprise/addons` y las imágenes se fijan por digest en `manager.py`.

QA conserva los datos de negocio y los accesos al momento de la copia: usuarios activos e inactivos, contraseñas, permisos por grupo/empresa, TOTP y passkeys. No renombra al administrador ni habilita empresas adicionales. Cambia UUID y elimina las sesiones para exigir un nuevo inicio de sesión. Desactiva cron, correo, automatizaciones, SMS, pagos, claves API y credenciales fiscales. Las passkeys conservan sus restricciones de origen del navegador; no se elimina el segundo factor para facilitar el acceso. Odoo y PostgreSQL de QA permanecen en redes internas; solamente su proxy tiene una segunda red para recibir el acceso publicado. La copia no es replicación continua ni devuelve cambios a producción: un cambio posterior de contraseña llega a QA con el siguiente `sync`.

## Comandos del operador

```bash
sudo bioteczac status
sudo bioteczac verify
sudo bioteczac backup
sudo /root/bioteczac_qa_manager.sh sync
```

`sync` reemplaza completamente QA a partir de producción. Detiene brevemente Odoo de producción para obtener una copia consistente de PostgreSQL y del filestore, vuelve a iniciar producción y realiza la restauración en QA. La neutralización termina antes de abrir QA. El proceso compara 24 tablas de negocio, verifica todos los archivos referenciados y compara huellas SHA-256 de cuentas, permisos y segundo factor antes y después de neutralizar. Si los accesos difieren del corte, QA permanece cerrado. No se imprimen ni archivan en claro las contraseñas o sus hashes individuales. `last-refresh.json` registra el corte y la comprobación de accesos. El bloqueo de mantenimiento impide ejecutar dos operaciones simultáneas. `setup` rechaza una producción ya inicializada y no la reinicia.

Para acceder antes de configurar el dominio:

```bash
ssh -N -L 1400:127.0.0.1:1400 -L 1401:127.0.0.1:1401 root@2.24.78.58
```

Abrir `http://localhost:1400` o `http://localhost:1401`. El transporte remoto queda cifrado por SSH. El host admite autenticación SSH por llave y tiene firewall y Fail2ban para SSH. Los secretos están bajo `secrets/` de cada entorno; no se incluyen en Git, argumentos del proceso ni imágenes.

### Acceso directo de producción y QA por IP

El acceso público autorizado adicional es `https://2.24.78.58:1400/odoo`. Conserva el mismo usuario y contraseña de producción. El puerto público 1400 termina TLS en Nginx (8443 dentro del contenedor); el origen privado HTTP en loopback sigue disponible para SSH o un futuro Cloudflare Tunnel. Una petición HTTP al puerto público redirige a HTTPS antes del inicio de sesión. QA tiene acceso público independiente en `https://2.24.78.58:1401/odoo`, autorizado posteriormente por el cliente. Cada entorno necesita su propio `public-access.json`; la configuración pública de producción no habilita QA automáticamente. El motor PostgreSQL y Odoo de QA conservan sus redes internas sin salida a Internet.

`production/public-access.json` y `qa/public-access.json` activan sus respectivos listeners al renderizar Compose/Nginx. El certificado se emite con Certbot 5.8 (snap oficial), perfil `shortlived`, validación HTTP-01 y nombre de certificado `bioteczac-ip`. El puerto 80 se reserva para el servidor temporal de validación de Certbot y no sirve Odoo. La renovación automática del snap llama al hook `/opt/bioteczac/runtime/publish_tls.py`, instalado en `/etc/letsencrypt/renewal-hooks/deploy/bioteczac-ip`. El hook verifica IP, cadena, vigencia y correspondencia de la llave, publica los archivos de forma atómica en directorios separados de cada entorno habilitado y recarga sus proxies. El certificado identifica la IP y cubre ambos puertos; cada proxy monta únicamente su copia local. La llave TLS no se monta en Odoo ni PostgreSQL. La regeneración de QA conserva su propia URL pública y sus secretos de infraestructura (PostgreSQL y gestor de bases), mientras los accesos de Odoo se copian de producción. Los archivos `login_password` son credenciales de arranque y no sustituyen las contraseñas que posteriormente cambien los usuarios.

Comprobar con `systemctl list-timers snap.certbot.renew.timer`, `certbot certificates` y `certbot renew --cert-name bioteczac-ip --dry-run --run-deploy-hooks`. Si se restaura en otro servidor, reemitir el certificado de la IP que corresponda antes de habilitar el listener. Al conectar Cloudflare se puede retirar el acceso público por IP eliminando expresamente `public-access.json`, renderizando de nuevo y recreando únicamente el proxy. No se debe abrir el origen HTTP de Odoo a Internet.

Referencias: [certificados de IP de Let's Encrypt](https://letsencrypt.org/2026/03/11/shorter-certs-certbot) y [renovación de Certbot](https://eff-certbot.readthedocs.io/en/stable/using.html#renewing-certificates).

## Respaldo y recuperación

El timer `bioteczac-backup.timer` genera un respaldo diario aproximadamente a las 03:00 de Monterrey (09:00 UTC). El comando `bioteczac backup` permite uno adicional. Consultar el resultado con `journalctl -u bioteczac-backup.service` y `systemctl list-timers bioteczac-backup.timer`.

Los archivos `backups/production-*.tar.age` contienen el dump PostgreSQL, filestore, configuración sin contraseñas, versiones de Git y controles al corte. Cada archivo tiene SHA-256. `qa-refresh` descifra y restaura el archivo cifrado real: sirve también para ensayar recuperación, sin modificar producción. La llave de recuperación está en `/opt/bioteczac/secrets/backup.agekey`; se entregó además una copia privada local. Conservar esta llave por separado de los respaldos. El respaldo de la antigua demo es `retired-demo-*.tar.gz.age` e incluye su clúster detenido y sus archivos; no pertenece a producción.

No hay destino de respaldo externo configurado todavía. Programar su copia cifrada fuera del servidor y acordar retención, alertas y tiempo de recuperación antes de incorporar información confidencial operativa. La recuperación sobre producción requiere una ventana de mantenimiento y una restauración previamente comprobada en QA; el comando cotidiano solo reemplaza QA.

## Fuente de la migración

Archivo privado: `Modelo_Clasificacion_v2_Remapeo.xlsx`.

SHA-256: `e8abe77d8f665bcc0ac025bc411352498c9ffb802b72f2c01a51703e2e4ea744`.

| Hoja | Contenido conservado / destino |
|---|---|
| `00_LEEME` | Instrucciones completas en el archivo y archivo JSON de todas las hojas |
| `01_DIM_DIVISION` | 3 divisiones |
| `02_DIM_GRUPO` | 11 grupos |
| `03_DIM_FAMILIA` | 56 familias, incluidos sus estados |
| `04_DIM_CLASIFICADOR` | 90 clasificadores reales; el texto introductorio del Excel menciona 89 |
| `05_REL_FAMILIA_CLAS` | 323 combinaciones autorizadas |
| `06_DIM_MARCA` | 17 marcas |
| `07_DIM_ESPECIALIDAD` | 17 especialidades |
| `08_DIM_EQUIPO` | 11 equipos |
| `09_DIM_SUBCLASE_MT` | 21 subclases terapéuticas |
| `20_REMAPEO` | 48 filas y sus 80 columnas, fórmulas y posición de origen; 42 claves distintas |
| `21_REL_PROD_ESPECIALIDAD` | 89 filas originales; 81 vínculos distintos |
| `22_REL_PROD_EQUIPO` | 58 filas originales; 50 vínculos distintos |
| `30_VALIDACION` | Controles, valores y fórmulas originales completos |
| `31_INCIDENCIAS` | 34 filas originales; incidencias pertinentes vinculadas a cada producto |

El XLSX íntegro y su representación de todas las hojas son adjuntos privados de la empresa principal. Cada ficha conserva sus renglones originales; el tab **Origen de la migración** permite consultarlos y descargar el archivo. El importador valida las relaciones antes de escribir y reconoce una repetición del mismo archivo mediante su huella, sin duplicar fichas ni sobrescribir ediciones posteriores.

Las seis claves repetidas se mantienen como fichas pendientes de revisión con todas sus variantes de origen. Cuatro fichas adicionales requieren aclarar la presentación. No se sumaron existencias ni se generaron recepciones: el archivo declara existencias cero. Se conservaron 27 nombres reales de fabricante/distribuidor, 13 unidades de origen y 5 tipos de empaque. No se inventaron equivalencias caja/pieza, RFC, impuestos, imágenes ni datos de contacto.

Los precios originales permanecen disponibles; el XLSX no declara su moneda ni confirma de manera uniforme la unidad comercial. Por ello la activación comercial requiere la revisión de Dirección. La confirmación no cambia el origen histórico.

## Datos de arranque y pendientes concretos

Quedan SEB Zacatecas, VALMA y PRO OMNIMEDIC, con RFC, razón social, domicilio y régimen fiscal proporcionados. La localización contable mexicana está instalada, sin asientos de apertura ficticios. No hay operaciones demo. Los almacenes técnicos creados por Odoo están archivados hasta definir ubicaciones físicas reales; no equivalen a delegaciones activas.

Pendientes del negocio: resolver duplicados y presentaciones, confirmar moneda/precios, configurar impuestos aplicables, almacenes/delegaciones reales y permisos de futuros usuarios. Pendientes de acceso: dominio y Cloudflare Tunnel/Access, respaldo externo y enrolamiento personal de segundo factor del administrador. No se forzó OTP por correo porque aún no existe SMTP configurado. Los logos quedan a cargo del cliente.

En Cloudflare, definir orígenes `http://127.0.0.1:1400` y `http://127.0.0.1:1401`, proteger especialmente QA con Access y actualizar `web.base.url`. Mantener el gestor de bases bloqueado. Configurar la confianza de `CF-Connecting-IP` únicamente para el conector autorizado antes de aplicar límites por IP pública; no confiar indiscriminadamente en cabeceras enviadas por Internet.

## Validación realizada

Ocho pruebas Odoo del asistente y del origen de migración: cero fallos. Inicio de sesión de soporte verificado en ambos entornos. Comprobados los 48 renglones asociados a 42 fichas, integridad de adjuntos, denegación real de CREATE DATABASE al rol aplicativo y bloqueo de red de QA hacia Internet y PostgreSQL de producción. Una marca creada solo en QA desapareció tras regenerar; producción no la recibió y los controles de negocio coincidieron al terminar.
