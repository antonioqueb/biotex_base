# Identidad fiscal del proyecto

Fuente: datos transcritos por el cliente el 6 de septiembre de 2026. No se adjuntaron en este turno los PDF originales; no se presentan como documentos verificados ante el SAT. Los nombres fiscales se capturan exactamente como fueron proporcionados, sin incorporar el régimen de capital al campo de razón social.

| Campo | SEB Zacatecas | VALMA | PRO OMNIMEDIC |
|---|---|---|---|
| Razón social | SERVICIOS Y EQUIPOS EN BIOTECNOLOGIA DE ZACATECAS | INGENIERIA EN EQUIPOS MEDICOS VALMA | PRO OMNIMEDIC |
| RFC | SEB150217A8A | IEM1809192W9 | POM210831IH5 |
| Régimen de capital | Sociedad Anónima de Capital Variable | Sociedad Anónima de Capital Variable | Sociedad Anónima de Capital Variable |
| Nombre comercial | SERVICIOS Y EQUIPOS EN BIOTECNOLOGIA DE ZACATECAS, S.A. DE C.V. | INGENIERIA EN EQUIPOS MEDICOS VALMA | PRO OMNIMEDIC |
| Inicio de operaciones | 2015-02-17 | 2018-09-19 | 2021-08-31 |
| Estatus informado | Activo | Activo | Activo |
| Fecha de constancia informada | 2026-09-02 | 2026-01-08 | 2026-01-08 |
| Calle y número | Calle Llano de la Isabelica #3000 | Calle Celso Cepeda #5029 | Av. Ignacio Zaragoza #730 |
| Interior | 0 | No proporcionado | 9 |
| Colonia | Fracc. Lomas de la Isabelica | Col. Plutarco Elías Calles | Col. Valle de las Trojes |
| Código postal | 98099 | 64108 | 20115 |
| Ciudad y estado | Zacatecas, Zacatecas | Monterrey, Nuevo León | Aguascalientes, Aguascalientes |
| Entre calles | No proporcionado | Ejército Nacional y Mina Voladora | Trigales y Praderas |
| Régimen fiscal | General de Ley Personas Morales (601) | General de Ley Personas Morales (601) | General de Ley Personas Morales (601) |

## Actividades informadas

| Actividad | SEB Zacatecas | VALMA | PRO OMNIMEDIC |
|---|---:|---:|---:|
| Comercio al por mayor de mobiliario, equipo e instrumental médico y de laboratorio | 100% | 60% | 40% |
| Construcción de inmuebles comerciales, institucionales y de servicios | — | 20% | — |
| Administración y supervisión de construcción de esos inmuebles | — | 5% | — |
| Laboratorios de pruebas | — | 10% | 10% |
| Comercio al por menor de aparatos ortopédicos | — | 5% | 10% |
| Comercio al por mayor de productos farmacéuticos | — | — | 20% |
| Otros consultorios privados para el cuidado de la salud | — | — | 10% |
| Reparación y mantenimiento de equipo electrónico y de precisión | — | — | 10% |

El cliente informó obligaciones de IVA e ISR para las tres empresas, incluidas declaraciones de proveedores de IVA, anual de ISR y pagos provisionales. Informó retenciones de ISR por sueldos y salarios para SEB y PRO OMNIMEDIC; para esta última, desde enero de 2023. Estos antecedentes se conservan como documentación y no generan tasas, retenciones por producto ni límites automáticos de operación.

## Alcance técnico

La versión 19.0.2.1.0 del módulo existente `biotex_base` corrige nombre fiscal, nombre corto, RFC, domicilio y régimen fiscal nativo cuando está instalada la localización mexicana. Conserva los mismos registros de empresa y contacto. Los datos complementarios de esta ficha quedan documentados aquí; no se crean campos ni módulos para simular una configuración fiscal adicional.

La migración verifica las tres identidades antes de escribir, registra valores anteriores y posteriores en el log y agrega referencias externas a las empresas secundarias existentes. No modifica cuentas bancarias, impuestos de productos, titularidad de documentos ni ubicaciones de almacenes. Las denominaciones antiguas se admiten exclusivamente como antecedentes para localizar registros con su RFC anterior.

El generador de ejemplos se corrige para usar estas identidades en futuras instalaciones. No se vuelve a ejecutar en la base existente.

## Cambio de nombre de la base

La base operativa pasa de `biotex` a `bioteczac` mediante cambio de nombre de la misma base PostgreSQL, junto con su directorio de adjuntos. Se conserva su OID, UUID, usuarios, documentos y saldos. La configuración de Odoo selecciona únicamente `bioteczac` para evitar abrir las copias antiguas. Los nombres técnicos de módulos, repositorios, contenedores y rutas permanecen estables.

El procedimiento detiene Odoo, respalda base, adjuntos, código y configuración, compara controles de operaciones y conserva instrucciones de reversión. Se ensaya sobre una restauración antes de producción. Los procedimientos históricos de `ops/` con fecha anterior describen la base con su nombre anterior y no deben reutilizarse para futuros despliegues.

Referencia del mecanismo de cambio de nombre: [PostgreSQL, ALTER DATABASE](https://www.postgresql.org/docs/current/sql-alterdatabase.html). La migración de módulos usa los scripts de actualización por versión de Odoo existentes en este proyecto.
