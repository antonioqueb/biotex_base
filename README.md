# SEB Zacatecas, VALMA y PRO OMNIMEDIC — Base

Módulo para **Odoo 19 Enterprise** · Alphaqueb Consulting SAS · Proyecto SEB Zacatecas.

Grupos de seguridad, delegaciones (almacenes), razones sociales e instituciones

## Dependencias
`base`, `mail`, `stock`, `purchase`

## Instalación
1. Clonar dentro del `addons_path` del servidor Odoo 19 junto con los demás módulos `biotex_*`.
2. Actualizar lista de aplicaciones e instalar `biotex_base`.

## Licencia
LGPL-3

## Identidad fiscal y actualización 19.0.2.1.0

Corrección de las tres empresas existentes según los datos proporcionados por el cliente el 6 de septiembre de 2026. La migración resuelve identidades por identificadores persistentes, RFC y antecedentes explícitos; rechaza coincidencias ambiguas y no crea empresas. Conserva los identificadores de empresa y contacto, documentos, cuentas y movimientos. El generador de ejemplos no se ejecuta durante esta actualización.

- [Manual de usuario](docs/manual.md)
- [Datos fiscales y alcance de la corrección](docs/identidad-fiscal.md)

Los identificadores técnicos `biotex_*` se conservan para no romper relaciones. El nombre operativo de la base es `bioteczac`.
