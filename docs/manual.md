# Manual de usuario de SEB Zacatecas, VALMA y PRO OMNIMEDIC

**Servicios y Equipos en Biotecnología de Zacatecas, S.A. de C.V.**  
**RFC:** SEB150217A8A  
**Versión del manual:** 1.2 · 6 de septiembre de 2026  
**Referencia de la aplicación:** Odoo 19; Base y Catálogo 19.0.2.1.0. Base de datos operativa: `bioteczac`.

Este manual explica cómo trabajar con catálogo, solicitudes, compras, inventario, pagos, contratos, remisiones y cobranza. Está dirigido a usuarios de operación, coordinación, compras, almacén, administración, contabilidad y dirección.

La guía se elaboró revisando las vistas y acciones del código correspondiente a la actualización publicada en GitHub. Algunos controles nuevos todavía no tienen una captura completa en pantalla. Esos casos se señalan junto al procedimiento y en la sección de pendientes. Este documento no acredita que todas las reglas de negocio hayan pasado pruebas funcionales con usuarios.

## Contenido

1. [Acceso y navegación](#acceso)
2. [Responsabilidades y rutas rápidas](#responsabilidades)
3. [Cómo se relacionan los registros](#registros)
4. [Catálogo de productos](#catalogo)
5. [Clientes, hospitales y proveedores](#contactos)
6. [Solicitudes de compra](#solicitudes)
7. [Cotizaciones y órdenes de compra](#compras)
8. [Recepciones, lotes y traspasos](#inventario)
9. [Solicitudes de pago y dinero registrado](#pagos)
10. [Contratos](#contratos)
11. [Ventas y remisiones](#remisiones)
12. [Máscaras y regularización](#mascaras)
13. [Facturas, cobros y cuentas abiertas](#cuentas)
14. [Operaciones entre empresas](#empresas)
15. [Excepciones operativas](#excepciones)
16. [Tableros y lectura de saldos](#indicadores)
17. [Correcciones y problemas frecuentes](#correcciones)
18. [Funciones pendientes de completar en pantalla](#pendientes)
19. [Rutina de trabajo y ejemplos](#rutina)
20. [Glosario, soporte y referencia de versión](#soporte)

<a id="acceso"></a>
## 1. Acceso y navegación

### Iniciar una sesión

1. Abra la dirección de la aplicación proporcionada por administración.
2. Ingrese con su usuario personal y contraseña. Si aparece un selector de base, utilice **bioteczac**. Después del cambio de nombre puede ser necesario iniciar sesión nuevamente; los usuarios y contraseñas se conservan.
3. Revise la empresa activa en el selector superior antes de crear un documento.
4. Abra la aplicación correspondiente desde el menú de aplicaciones.

Los menús y botones dependen de sus permisos. Una persona puede tener varias funciones, pero debe usar su propia cuenta para conservar su autoría. Solicite a administración los permisos faltantes indicando la tarea y el ámbito de empresa/delegación.

### Buscar y consultar

- Use el buscador de cada lista para localizar folios, productos o contrapartes.
- Revise los filtros activos. **Mis solicitudes**, **Pagadas**, **Sin firma** y otras entradas abren selecciones específicas; un registro puede existir aunque no aparezca en esa selección.
- Use **Agrupar por** para revisar proveedor, empresa, estado o delegación cuando la vista lo permita.
- En las listas, el selector de columnas permite mostrar datos opcionales, como unidades o cantidades recibidas.
- Los botones con contadores, como **Órdenes**, **Traspasos** o **Remisiones**, abren documentos relacionados.

Antes de volver a crear un documento aparentemente faltante, búsquelo por folio y quite los filtros pertinentes. Si aparece un error al confirmar, vuelva a consultar el registro y sus vínculos antes de repetir la acción.

### Guardar notas y evidencia

Guarde la captura antes de avanzar de etapa. En el área de conversación del registro puede usar **Registrar nota** y adjuntar archivos originales. Identifique qué respaldan: cotización, autorización, guía, recepción, firma, factura o comprobante.

**Enviar mensaje** puede notificar a los seguidores del registro; úselo cuando corresponda comunicar algo. Una nota o un archivo adjunto no sustituye un campo obligatorio, una autorización ni la confirmación de un hecho.

Conserve la fecha real del evento y explique las diferencias con la fecha del documento o de captura. Para corregir registros confirmados, siga [Correcciones](#correcciones).

<a id="responsabilidades"></a>
## 2. Responsabilidades y rutas rápidas

### Funciones

| Función | Trabajo habitual |
|---|---|
| Delegación / ventas | Registrar necesidades, consultar su seguimiento y preparar remisiones de su ámbito. |
| Coordinación | Revisar sustento, cantidades y destino; autorizar solicitudes. |
| Compras | Buscar abastecimiento, preparar cotizaciones y órdenes, coordinar traspasos y guías. |
| Almacén | Verificar artículos, cantidades y lotes; validar movimientos físicos con los permisos de Inventario. |
| Administración / Pagos | Revisar beneficiario, autorizar importes y registrar el dinero correspondiente. |
| Contabilidad | Revisar documentos económicos, aplicaciones, CxP y CxC. |
| Dirección | Administrar estructura y ámbitos, autorizar excepciones y revisar consolidados. |
| Clasificador de catálogo | Completar fichas, fotografías y clasificación mediante los asistentes. |

El permiso de delegación no concede por sí solo todos los permisos nativos de Inventario. Quien valide recepciones o salidas necesita también la autorización correspondiente en Inventario.

### Dónde realizar cada tarea

| Necesidad | Ruta principal |
|---|---|
| Consultar artículos | **Catálogo → Productos** |
| Clasificar varios artículos | **Catálogo → Asistente de clasificación** |
| Clasificar uno por uno | **Catálogo → Asistente guiado (1 a 1)** |
| Registrar una necesidad | **Solicitudes → Solicitudes de compra** |
| Revisar lo propio | **Solicitudes → Mis solicitudes** |
| Autorizar necesidades | **Solicitudes → Por autorizar** |
| Consultar compras | **Compras → Pedidos → Solicitudes de presupuesto / Órdenes de compra** |
| Dar de alta un proveedor | **Compras → Pedidos → Alta rápida de proveedor** |
| Consultar embarques | **Compras → Pedidos → Guías en tránsito** |
| Revisar precios | **Compras → Informes → Historial de precios** |
| Atender pagos | **Pagos → Cola de pagos** |
| Consultar deuda con proveedores | **Pagos → Cuentas por pagar consolidadas** |
| Consultar contratos | **Contratos → Contratos / Avance por clave** |
| Registrar entregas | **Remisiones → Remisiones** |
| Atender firmas pendientes | **Remisiones → Sin firma** |
| Revisar facturación y cobranza | **Cobranza → Remisiones por facturar / Facturas de cliente / Cuentas por cobrar** |
| Revisar traspasos | **Solicitudes → Traspasos** |
| Registrar una excepción | **Inventario → Excepciones operativas** |

Las aplicaciones estándar pueden aparecer como **Facturación** o **Contabilidad**, según la configuración y los permisos. Algunos accesos de la aplicación también se repiten dentro de Ventas, Compras e Inventario.

<a id="registros"></a>
## 3. Cómo se relacionan los registros

La operación tiene varias dimensiones. Compruebe cada una en su documento de origen.

| Registro | Qué representa | Qué debe comprobarse por separado |
|---|---|---|
| Solicitud de compra | La necesidad y su autorización. | Compra, recepción y pago. |
| Orden de compra | El compromiso con el proveedor. | Mercancía recibida y dinero pagado. |
| Recepción de inventario | La entrada física validada. | Factura y pago al proveedor. |
| Solicitud de pago | El importe que se pide autorizar. | Pago real y aplicación a la obligación. |
| Pago / cobro | El registro de una salida / entrada de dinero. | Su aplicación y la mercancía correspondiente. |
| Contrato | Los compromisos documentados con el cliente. | Entregas, documentos económicos y cobros. |
| Remisión | Los artículos incluidos en una entrega; su realización se comprueba con el movimiento validado. | Aceptación, facturación y cobranza. |
| Máscara | La correspondencia administrativa entre una entrega y sus documentos. | Identidad física, sustento de diferencias y dinero. |
| Factura registrada | El documento económico y su saldo contable. | Movimiento físico y dinero recibido o pagado. |

El recorrido habitual es: **necesidad → autorización → abastecimiento → recepción → entrega**. En paralelo se revisan **obligación → pago** y **documento de venta → cobro**. Los contratos y las máscaras explican las relaciones administrativas.

Para reconstruir una operación, conserve los folios relacionados y consulte las cantidades por renglón. Un enlace al encabezado no explica por sí solo una entrega parcial.

<a id="catalogo"></a>
## 4. Catálogo de productos

### Localizar y revisar un artículo

1. Entre a **Catálogo → Productos**.
2. Busque por nombre o clave. Consulte también la referencia del fabricante, el código anterior y los sinónimos de la ficha.
3. Abra el producto y revise la pestaña **Clasificación**.
4. Verifique presentación, contenido, medidas, marca, fabricante, modelo y equipo compatible antes de elegirlo para una solicitud.

Un producto parecido o compatible puede ser un artículo distinto. Si encuentra un posible duplicado, remítalo al responsable de catálogo con ambas claves; no cree otra ficha ni acumule sus existencias para resolver la duda.

Para un artículo nuevo, el usuario autorizado puede usar **Productos → Nuevo** después de comprobar que no existe. Complete la ficha disponible y continúe su clasificación sobre ese mismo registro.

### Completar una ficha

Capture la información disponible y comprobable:

| Grupo de datos | Qué revisar |
|---|---|
| Clasificación | División, grupo, familia, clasificador y marca. |
| Descripción | Denominación del artículo, medidas, contenido y notas de uso. |
| Identidad de origen | Referencia del fabricante, modelo, código alterno y código anterior de SICAR cuando exista. |
| Presentación | Tipo de empaque, contenido por presentación y unidad usada en la operación. |
| Datos técnicos | Fabricante, país de origen, especialidad y equipos compatibles. |
| Datos comerciales | Proveedor, precios registrados e impuestos que corresponda revisar con administración. |

La presentación comercial y la unidad de inventario deben ser coherentes. Si no está validada la conversión caja–pieza, deje la operación pendiente de aclaración. Los precios adicionales de la ficha no garantizan que todas las ventas apliquen automáticamente una lista de precios.

### Fotografías y documentos

La ficha dispone de una imagen principal, **Foto 2** y **Foto 3**. Puede cargarlas sin esperar a terminar la clasificación y conservarlas al actualizar la misma ficha. Compruebe que está editando el producto correcto antes de subir cada archivo.

Estos tres espacios describen la pantalla actual; no constituyen un máximo de fotografías aprobado para todas las familias. Puede conservar evidencia adicional como adjuntos, aunque no aparezca en esos espacios de imagen.

Adjunte certificados y referencias originales al producto o lote que corresponda. Si el documento es de otro lote, identifíquelo como antecedente. Dirección dispone de una excepción de fotografía cuando proceda, que debe sustentarse.

### Asistente guiado, un artículo a la vez

1. Abra **Catálogo → Asistente guiado (1 a 1)**.
2. Seleccione grupo, familia, clasificador y marca.
3. Complete descripción, medidas, presentación y fotografías disponibles.
4. Revise la descripción y clave propuestas.
5. Use **Guardar** para terminar o **Guardar y siguiente** para continuar con otro artículo.

### Clasificación de varios productos

1. Abra **Catálogo → Asistente de clasificación**, o seleccione productos y use **Clasificar con asistente**.
2. Defina la clasificación compartida.
3. Busque y agregue únicamente los productos que correspondan a esa selección. El buscador muestra hasta veinte resultados por página y excluye los ya agregados. Puede seleccionar con las flechas y usar **Enter** para agregar; el foco regresa al buscador.
4. Revise la lista y abra cada renglón que requiera una particularidad. Compruebe referencias, medidas y presentación.
5. Revise el orden y las claves antes de pulsar **Generar claves**. Si un producto ya tiene otra referencia, se muestra una comparación de referencia anterior y nueva. Revise los cambios y marque la aceptación para confirmar la reclasificación.
6. Si necesita continuar después, use **Guardar y salir** y retome la sesión desde **Sesiones de clasificación**.

Una sesión confirmada conserva sus resultados y queda bloqueada para su edición ordinaria. Para una corrección posterior, solicite revisión de catálogo. Cambiar la clasificación puede cambiar claves visibles: conserve la equivalencia con la clave anterior y los documentos originales.

Las tablas de búsqueda y productos agregados tienen desplazamiento interno y encabezados fijos. Cambiar el orden de las filas del asistente conserva sus consecutivos reservados; cambiar la clasificación de la sesión sí puede cambiar las referencias propuestas.

El lápiz de cada renglón abre **Editar producto clasificado**. Revise **Datos principales** y despliegue **Información adicional** cuando necesite modificar presentación, referencias o datos técnicos. Use **Guardar cambios** para volver a la lista. Los cambios de nombre y unidad deben quedar guardados antes de generar claves o salir; el asistente señala cualquier error pendiente.

Las aplicaciones nuevas conservan usuario, fecha y clasificación anterior y nueva en **Sesiones de clasificación → Historial de clasificación** y como nota en el producto. Si alguien modifica el producto después de abrir la comparación, el sistema solicita una revisión nueva antes de aplicar. Los antecedentes previos conservan sus datos disponibles; no se inventa su autoría histórica.

### Estados de catálogo

| Estado | Cómo interpretarlo |
|---|---|
| Sin clasificar | Faltan datos que exige el clasificador actual. |
| Clasificado sin foto | La clasificación está cubierta, pero falta la condición de fotografía. |
| Completo | Cumple los requisitos que actualmente calcula la ficha. |

**Completo** no certifica validación técnica, compatibilidad ni documentación del lote. El cálculo actual exige medidas de forma general; si no aplican, deje el caso para revisión en lugar de inventar una medida. Los estados independientes de validación técnica siguen pendientes de completar.

Desde la ficha puede usar **Etiqueta QR**; las listas también ofrecen impresión de etiquetas. Compruebe producto y clave antes de colocar una etiqueta física.

### Administrar la estructura y las referencias

En **Catálogo → Configuración**, Dirección administra **Divisiones y grupos**, **Familias** y **Clasificadores**. Los usuarios autorizados también pueden consultar **Marcas**, **Equipos compatibles**, **Tipos de empaque**, **Especialidades** y **Subclases terapéuticas**.

Antes de crear una marca, búsquela y revise las coincidencias sugeridas por el asistente. Conserve la denominación y el código aprobados. Para una compatibilidad, agregue el equipo correcto a la ficha y conserve el soporte técnico y su responsable. **Catálogo → Genéricos** permite consultar las agrupaciones existentes; compartir un genérico no vuelve intercambiables todos sus productos.

<a id="contactos"></a>
## 5. Clientes, hospitales y proveedores

### Cliente e institución

Use **Contratos → Instituciones y clientes** para consultar o completar razón social, RFC, datos de contacto y tipo de cliente. La empresa principal utiliza el RFC **SEB150217A8A**. Las otras empresas deben conservar su identidad propia.

Registre el hospital o destino como la dirección de entrega correspondiente al cliente cuando así esté configurado. La remisión permite seleccionar destinos relacionados con ese cliente. Si falta el hospital, solicite el alta y la revisión de su relación antes de confirmar la entrega.

El hospital receptor no se convierte automáticamente en el deudor de la factura. Administración debe verificar la entidad receptora del documento económico.

### Alta rápida de proveedor

1. Abra **Compras → Pedidos → Alta rápida de proveedor**.
2. Capture nombre y tipo de persona, teléfono, correo o WhatsApp disponibles.
3. Registre la condición acordada de contado o crédito, plazo de entrega y si requiere orden formal.
4. Capture RFC y notas cuando se disponga de ellos.
5. Guarde y revise la ficha completa antes de emitir una orden o solicitar un pago.

En **Condiciones de proveedor** se consultan datos pendientes, horarios, condiciones y observaciones. Marcar una ficha como completa no sustituye la verificación de identidad y cuenta del beneficiario.

La condición de pago de la compra se muestra a partir del proveedor. Evite modificar la ficha general para aparentar una condición distinta en una operación histórica; documente el acuerdo del caso y solicite su revisión.

<a id="solicitudes"></a>
## 6. Solicitudes de compra

### Registrar la necesidad

1. Abra **Solicitudes → Solicitudes de compra → Nuevo**.
2. Seleccione la delegación/almacén de destino, solicitante y fecha requerida. Marque la urgencia cuando corresponda.
3. Seleccione el sustento: contrato, compra emergente, cliente privado, abastecimiento de stock o regularización, según el caso disponible.
4. Capture el contrato cuando exista, el cliente que corresponda y la referencia de la compra emergente.
5. Revise empresa compradora y empresa vendedora cuando tenga acceso a esos campos. Si la pantalla pide motivo para una compradora diferente de la predeterminada, explique la operación real.
6. En **Productos**, agregue producto, cantidad y unidad. Muestre la columna de unidad si está oculta.
7. Complete referencia, marca/modelo de equipo, fotografía y observaciones necesarias por renglón.
8. Use **Notas para compras** para las condiciones de entrega y requisitos compartidos. Adjunte el sustento al registro.
9. Guarde y use **Enviar a autorización**.

La pantalla todavía utiliza el almacén en campos llamados «Delegación». El destino hospitalario y la delegación comercial tienen una captura incompleta en este formulario. Deje la información explícita en las notas y solicite completar el vínculo cuando sea necesario; las notas no sustituyen esa relación estructurada.

### Necesidad sin producto identificado

Puede describir el artículo pendiente, agregar referencia, equipo y fotografía. La línea queda identificada como pendiente.

**Resuelva la identidad antes de autorizar en esta versión.** Después de la autorización, el control de integridad bloquea cambios de producto y cantidades aunque la tabla parezca editable. Si ya se aprobó una línea sin identificar, coordinación debe gestionar una corrección documentada con soporte.

### Autorizar o solicitar aclaración

Coordinación entra a **Solicitudes → Por autorizar**, revisa necesidad, sustento, cantidades, destino y anexos, y usa **Autorizar sustento** si la información es suficiente.

**Regresar a borrador** exige un motivo de aclaración que todavía no está expuesto en el formulario. Si la acción lo solicita, conserve el comentario en el historial y remita el folio a soporte para completar la corrección. La nota por sí sola no satisface ese campo.

Compras puede iniciar la cotización de una urgencia antes de terminar la autorización cuando el sistema lo permita. La urgencia no sustituye la autorización requerida para generar y confirmar el abastecimiento.

### Consultar abastecimiento y avances

Revise las existencias de cada renglón antes de comprar. La consulta ayuda a proponer un traspaso; no constituye una reserva. Compruebe reservas, ubicación y disponibilidad utilizable con almacén.

Use **Órdenes** y **Traspasos** para consultar los documentos relacionados. Revise las columnas ordenadas y recibidas, y consulte los pagos por separado. Una compra a crédito puede estar recibida y seguir pendiente de pago.

Para dividir el suministro, conserve la cantidad correspondiente a cada origen. Si **Cotizar / ordenar** deja de aparecer después de una primera orden o recepción parcial, solicite a compras y soporte continuar sobre la misma necesidad; no registre una segunda solicitud que duplique el saldo.

### Cancelar una necesidad

Use **Cancelar**, seleccione el motivo y explique qué cantidad deja de requerirse. Revise por separado las compras, traspasos, pagos y entregas ya relacionados.

> El asistente conserva un aviso antiguo que menciona cancelar otros documentos. La acción actual cancela la solicitud; las demás operaciones requieren su resolución propia. Compruebe el estado de cada una.

Una solicitud con autorización o documentos relacionados puede rechazar **Reabrir**. Conserve el folio y solicite la corrección correspondiente.

<a id="compras"></a>
## 7. Cotizaciones y órdenes de compra

### Generar solicitudes de presupuesto

1. Abra una solicitud autorizada y pulse **Cotizar / ordenar**.
2. Revise productos y cantidades. Consulte existencias y proveedores sugeridos.
3. Seleccione proveedores y capture el precio estimado disponible.
4. Active **Enviar RFQ por correo a los proveedores** únicamente cuando corresponda enviar la solicitud: esa opción puede producir un envío real.
5. Pulse **Generar RFQ / OC**.
6. Abra los documentos generados desde **Órdenes** y revise cada uno.

La acción crea solicitudes de presupuesto en borrador. Elegir varios proveedores puede generar alternativas para la misma necesidad; revise cuáles serán confirmadas para evitar comprarla varias veces. Antes de repetir el asistente, busque los documentos que ya creó.

La descripción de la necesidad, referencias, equipo y notas se trasladan a las líneas de compra. Revise el resultado y consulte la solicitud original para sus anexos.

### Comparar ofertas

Consulte **Compras → Informes → Historial de precios** y las cotizaciones recibidas. Compare presentación, unidad, moneda, impuestos, flete, disponibilidad, plazo y condición de pago.

El promedio mostrado actualmente no garantiza una conversión homogénea entre todas las presentaciones y unidades. Verifique la base antes de usarlo como referencia. Si el precio requiere justificación, explique la oferta elegida con su soporte; no cambie cantidades o presentación para evitar la validación.

### Confirmar la orden

1. Abra la solicitud de presupuesto elegida.
2. Revise proveedor, empresa compradora, moneda y almacén de destino.
3. Compruebe producto real, referencia, unidad, cantidad, precio, descuentos, impuestos y flete.
4. Registre condiciones y justificaciones requeridas.
5. Guarde y use **Confirmar orden** o el botón equivalente de Compras.
6. Consulte el documento imprimible y verifique sus datos antes de enviarlo.

La confirmación controla las cantidades relacionadas con la necesidad. Si se excede el saldo, revise otras órdenes y traspasos antes de ampliar o corregir el compromiso. Para una sustitución real de producto, solicite validación del responsable de la necesidad; no cambie únicamente la descripción de otro artículo.

### Contado y crédito

- **Contado:** la confirmación puede generar la solicitud de pago de la orden. Revise **Pagos → Cola de pagos** antes de crear otra.
- **Crédito:** la recepción puede ocurrir antes del pago. Registre vencimiento y condición acordados en el documento del proveedor.

Los plazos de crédito se toman del acuerdo correspondiente. Los ejemplos de treinta días no son una política universal.

### Comunicación y guías

La acción de WhatsApp prepara un texto y abre WhatsApp; revise destinatario y contenido y efectúe el envío allí si corresponde. Abrir la conversación no demuestra entrega ni lectura del mensaje.

Desde los documentos de inventario asociados se registran paquetería, guía, enlace de rastreo y gastos por cobrar. **Capturar la guía puede poner el embarque en tránsito automáticamente**: utilice esa captura cuando corresponda al estado real y explique cualquier diferencia.

En **Guías en tránsito**, **Llegó la paquetería** registra la llegada operativa. Almacén aún debe revisar y validar la recepción física.

<a id="inventario"></a>
## 8. Recepciones, lotes y traspasos

### Recibir una compra

1. Abra la recepción vinculada a la orden, o localícela en **Inventario → Operaciones → Recepciones**.
2. Verifique proveedor/origen, empresa, ubicación de destino y productos.
3. Cuente y revise el material. Capture la cantidad efectivamente recibida en el movimiento.
4. Para productos con seguimiento, distribuya las cantidades entre los lotes reales. Registre caducidad donde esté habilitada y corresponda.
5. Adjunte remisión del proveedor, guía y documentación pertinente.
6. Valide únicamente la cantidad comprobada con **Validar**.
7. Si queda saldo por recibir, conserve la entrega pendiente mediante el documento parcial o pendiente que corresponda.

Una factura adjunta no registra la entrada física. Los artículos dañados, no identificados o con documentos discrepantes deben reportarse y colocarse en la ubicación o condición de revisión autorizada. No presuponga que todas las reglas de caducidad y bloqueo ya están configuradas.

### Recepción parcial

Si se ordenaron diez unidades y llegaron seis, capture seis. Mantenga las cuatro restantes pendientes y registre faltantes, daños o rechazo con su motivo. Si el proveedor ya no entregará el saldo, compras debe resolver el cierre del compromiso; no valide las cuatro faltantes como recibidas.

### Traspasar entre almacenes

1. Desde una solicitud autorizada, revise la existencia en otras ubicaciones.
2. Compras abre **Traspaso desde otra delegación**, selecciona origen y cantidades y revisa el destino.
3. Consulte los movimientos en **Traspasos**.
4. El almacén de origen registra y valida la salida real hacia tránsito.
5. El destino registra y valida lo que recibe desde tránsito.

El recorrido utiliza dos movimientos: origen–tránsito y tránsito–destino. El asistente actual admite almacenes de la misma empresa y requiere una ubicación de tránsito configurada. Si falta, solicite su configuración.

Si salen diez y llegan ocho, las dos restantes deben seguir identificadas en tránsito o en la incidencia correspondiente. El documento de llegada no se valida por diez para cerrar el traspaso.

### Devoluciones y ajustes

Almacén debe iniciar la devolución vinculada al movimiento original, identificar línea, cantidad, lote, motivo y destino del material. Administración revisa por separado la nota, el reembolso o el saldo a favor que corresponda.

Si la mercancía ya estaba facturada o conciliada mediante una máscara, avise a contabilidad y contratos con los folios afectados. El seguimiento completo de las aplicaciones después de una devolución todavía requiere revisión del responsable.

Los ajustes de inventario se reservan para diferencias de conteo autorizadas. No los use para simular una compra, entrega o devolución.

<a id="pagos"></a>
## 9. Solicitudes de pago y dinero registrado

### Revisar la solicitud

1. Entre a **Pagos → Cola de pagos**.
2. Abra la solicitud y verifique orden, empresa, proveedor, moneda, vencimiento y monto.
3. Revise otras solicitudes y pagos de la misma compra antes de autorizar.
4. Administración verifica cuenta o medio del beneficiario y conserva el soporte del acuerdo.

Una nueva solicitud manual necesita una compra confirmada para avanzar mediante **Solicitar pago** en la implementación actual. No presuponga que ya existe una captura completa para cualquier concepto ajeno a una orden.

### Aprobar el importe

En estado solicitado, administración captura **Importe aprobado** y pulsa **Aprobar**. Puede ser menor que lo solicitado. El sistema contrasta la autorización con otras autorizaciones y pagos vinculados a la compra.

| Campo | Significado actual |
|---|---|
| Monto a pagar | Importe solicitado. |
| Importe aprobado | Cantidad autorizada expresamente. |
| Dinero confirmado | Suma de los pagos vinculados que alcanzaron el estado confirmado como pagado. |
| Aprobado pendiente | Importe aprobado menos dinero confirmado, con mínimo cero. |
| Estado de ejecución | Sin dinero confirmado, Pago parcial, Cubierto o Antecedente por conciliar. |

Ejemplo: solicitado **10,000**, aprobado **4,000** y confirmado **1,500**. Quedan **2,500** aprobados por ejecutar y **6,000** de la solicitud sin aprobar. Este último importe se explica por diferencia; no es el campo **Aprobado pendiente**.

Después de aprobar, no hay una acción ordinaria completa para ampliar esa misma autorización parcial. Administración debe revisar el saldo y coordinar la ampliación documentada con soporte. No reduzca artificialmente el importe solicitado para cerrar la solicitud.

### Distinguir los dos botones «Registrar pago»

La pantalla conserva dos botones con ese nombre:

| Acción | Cómo reconocerla | Resultado |
|---|---|---|
| Abrir el pago contable | Aparece en una solicitud aprobada y abre un formulario de pago. | Permite preparar el registro vinculado a la solicitud. |
| Cerrar la solicitud como cubierta | Aparece como acción destacada y comprueba el dinero registrado. | Solo marca la solicitud pagada cuando el importe solicitado ya está cubierto. |

La segunda acción no registra dinero. Si muestra que falta confirmar el pago, revise el formulario de pago relacionado y su estado. Una aprobación parcial ejecutada por completo puede dejar abierta la solicitud total.

### Registrar el dinero con su evidencia

1. Desde la solicitud aprobada, use la acción que abre el formulario de pago.
2. Verifique empresa, beneficiario, moneda e importe; para una parcialidad, capture únicamente el importe real.
3. Revise fecha, diario y medio. Registre la referencia real y adjunte el comprobante en la sección **Comprobante** de la solicitud.
4. Complete la validación contable correspondiente al hecho real.
5. Regrese a la solicitud y compruebe **Dinero confirmado** y **Aprobado pendiente**.

La referencia de la solicitud no se copia automáticamente al campo de referencia exigido en el pago contable. Si ese campo no está disponible en su formulario, deje el pago pendiente y solicite completar la captura con soporte. El texto de concepto o memo no debe darse por equivalente sin comprobarlo.

Los pagos en proceso todavía pueden no aparecer en **Dinero confirmado**. Revise también borradores y pagos en proceso antes de abrir otro: el saldo mostrado no descuenta todos esos estados intermedios.

Registrar un pago en Odoo no ejecuta por sí mismo una transferencia bancaria. La configuración de diarios y cuentas transitorias determina sus efectos contables: sin las cuentas correspondientes, un pago puede no producir el asiento o la aplicación esperados. Contabilidad debe revisar esta configuración antes de usar pagos independientes. Véase la [documentación oficial de pagos de Odoo 19](https://www.odoo.com/documentation/19.0/applications/finance/accounting/payments.html).

### Anticipos y antecedentes

Un anticipo conserva su pago original. Cuando llega la obligación definitiva, contabilidad aplica el dinero existente; no registra otra salida por ese acto.

**Antecedente por conciliar** identifica una solicitud histórica marcada pagada que no tiene el vínculo nuevo con un pago contable. Revise comprobantes y registros originales con contabilidad. No vuelva a pagar ni registre un pago duplicado para cambiar el indicador.

La cancelación exige un motivo cuyo campo puede estar oculto cuando está vacío. Si no puede capturarlo, solicite apoyo. Una solicitud con dinero relacionado requiere revisar cada pago y su corrección propia.

<a id="contratos"></a>
## 10. Contratos

### Consultar el expediente

Abra **Contratos → Contratos** y revise empresa adjudicataria, institución, folio, fechas, modalidad de entrega, moneda e importe. En **Claves del contrato**, consulte clave institucional, descripción, unidad, cantidad y precio por línea. En **Documentos y notas**, conserve el contrato y sus anexos originales.

Use **Remisiones** para recorrer las entregas relacionadas y **Avance por clave** para revisar el detalle. Compare siempre el indicador con los documentos que lo originan.

### Preparar un contrato nuevo

1. Cree el registro en borrador y capture los datos documentados del encabezado.
2. Agregue las líneas adjudicadas con su clave, descripción, unidad, cantidad y precio.
3. Adjunte el documento de sustento y registre los datos que falten por validar.
4. Solicite al responsable la revisión previa a activar.

> **Limitación actual:** **Activar** requiere una referencia externa que aún no está expuesta en el formulario. La captura de hospitales autorizados, numeración de partidas y otros datos nuevos también está incompleta. El alta puede prepararse en borrador; completar su activación requiere apoyo de soporte y validación del responsable.

No use fechas, importes ni contratos ficticios para habilitar una entrega. Una clave institucional puede corresponder a varios productos internos, pero esa correspondencia todavía no tiene un recorrido completo en la interfaz.

### Modificar, ampliar o cerrar

Las condiciones de un contrato activo se protegen contra edición directa. Una ampliación requiere documento, aprobación y vigencia; el formulario de modificaciones versionadas sigue pendiente de completar. Remita el caso al responsable de contratos con la situación anterior y la modificación aprobada.

El campo visible de tolerancia no autoriza superar el límite contractual vigente. Los porcentajes de alerta y los ejemplos de ampliación deben validarse por contrato.

**Cerrar** atiende el estado administrativo; revise entregas, documentos y cobros abiertos antes de hacerlo. **Volver a borrador** puede aparecer en registros antiguos, pero la protección actual impide usarlo para borrar el antecedente de un contrato confirmado.

### Interpretar el avance

El valor administrativo aplicado y la cantidad física demostrable son conceptos distintos. Una cantidad contractual en cero puede reflejar que falta una correspondencia validada, aunque existan remisiones físicas. Los rótulos antiguos, como «Remisionado», deben contrastarse con el detalle de aplicaciones y movimientos.

<a id="remisiones"></a>
## 11. Ventas y remisiones

### Cotización o pedido comercial

Cuando se utilice Ventas, registre y revise la cotización con cliente, empresa, productos, unidades, precios y condiciones antes de confirmar el compromiso comercial.

La conversión automática entre todos los pedidos estándar de Ventas, solicitudes de abastecimiento y remisiones todavía no está completa. Coordinación debe definir el documento físico que atenderá la operación y conservar los folios comerciales relacionados. Antes de crear una remisión, compruebe si ya existe una salida del pedido para evitar despachar dos veces la misma entrega.

### Preparar la remisión

1. Entre a **Remisiones → Remisiones → Nuevo**.
2. Seleccione el sustento de la venta, el contrato cuando corresponda y el cliente.
3. Seleccione el hospital o dirección de entrega correcto.
4. Revise empresa responsable, almacén, fecha y referencia comercial.
5. En **Productos entregados**, capture los artículos físicos, cantidades, unidades y precios comerciales de esa entrega.
6. Revise disponibilidad y agregue observaciones necesarias.
7. Guarde y pulse **Confirmar**.

**Confirmar** prepara el movimiento asociado; la salida se acredita al validar el movimiento de inventario. La remisión puede confirmarse sin una máscara. La clave contractual no debe reemplazar al artículo físico de la línea.

El texto de lote de la remisión es informativo. Para la trazabilidad de existencias, los lotes y cantidades deben quedar registrados en el movimiento de inventario vinculado.

### Validar la salida y registrar la entrega

1. Abra el movimiento vinculado a la remisión. **Marcar entregada** puede abrirlo si sigue pendiente.
2. Almacén verifica producto, cantidad, reserva, ubicación y lotes reales.
3. Almacén valida la salida efectivamente realizada con sus permisos de Inventario.
4. El usuario con permiso de Inventario regresa a la remisión y usa **Marcar entregada** para reconocer el movimiento ya validado.
5. Compruebe fecha, destino y cantidades contra el soporte físico.

Imprimir, registrar una firma o volver a consultar el documento no debe utilizarse como sustituto de la validación de inventario.

### Entregas parciales

Para una entrega parcial planeada, prepare una remisión por la cantidad que realmente se entregará y conserve el saldo comercial por atender.

Si una remisión ya confirmada se despacha parcialmente, conserve el movimiento real y sus pendientes y avise al responsable. **El formato actual puede seguir mostrando las cantidades originales de la remisión**, aunque el movimiento sea parcial. Solicite conciliar el documento antes de presentarlo como entrega completa; no valide cantidades faltantes para hacer coincidir la impresión.

### Firma y documentos

En **Firma del cliente**, capture receptor y firma cuando se disponga de ellos y use **Registrar firma**. También puede adjuntar el documento firmado original. Un archivo adjunto por sí solo no completa todos los campos de aceptación.

Use **Remisiones → Sin firma** para revisar pendientes documentales. Si existe aceptación parcial o rechazo, conserve la evidencia y solicite revisar las cantidades y el retorno correspondiente.

**Imprimir remisión** genera el formato operativo. Revise productos, cantidades, destino y empresa antes de entregarlo. Conserve el PDF emitido como evidencia: algunos textos de impresión todavía se obtienen de la ficha actual del producto y pueden cambiar al reclasificarlo.

### Entrega directa o pendiente de regularización

Los controles para estos casos requieren vínculos que aún no se capturan completos en el formulario:

- **Entrega directa:** necesita relacionar el movimiento real proveedor–destinatario. La casilla por sí sola no completa la ruta.
- **Pendiente de regularización:** necesita una excepción autorizada y su vínculo, además de mercancía, receptor, valor y responsable.

Prepare el expediente con administración y soporte antes de confirmar estos casos. Conserve la ruta real y los documentos originales; no cree una entrada y salida central que no ocurrieron ni seleccione un contrato ajeno para avanzar.

<a id="mascaras"></a>
## 12. Máscaras y regularización

### Qué representa una máscara

La máscara explica cómo una porción de una entrega real corresponde con líneas contractuales y documentos económicos. Puede existir una diferencia de nombre, presentación o producto, pero cada caso necesita su sustento.

| Correspondencia | Qué se necesita demostrar |
|---|---|
| Alias del mismo artículo | Identidad del producto. |
| Presentación o unidad distinta | Conversión válida y cantidades comparables. |
| Sustitución de producto | Autorización y soporte específico; coincidir en dinero no demuestra equivalencia física. |

Aplicar un importe no crea una nueva salida, factura ni entrada de dinero. Para una sustitución, no obtenga una supuesta cantidad física dividiendo importes entre el precio de otro producto.

### Qué permite consultar la pantalla actual

La remisión con contrato conserva la pestaña **Claves a cobrar (máscara)** y el botón **Proponer claves**. Una propuesta requiere revisión; no es prueba de suministro ni autorización de sustitución.

Los nuevos estados de soporte, validación, aplicación, revisión y reversión todavía no tienen todos sus campos y botones en la interfaz. Tampoco existe un recorrido completo para repartir libremente entre varios contratos desde el formulario actual.

**No use la tabla antigua como confirmación de una nueva aplicación completa.** Si el sistema solicita importe de origen, documento destino o evidencia sin ofrecer dónde capturarlos, remita el caso al responsable de contratos y soporte.

### Preparar el expediente para conciliar

1. Identifique empresa, cliente/deudor, hospital y contrato.
2. Relacione las remisiones originales y el movimiento físico de cada una.
3. Identifique el documento económico y las líneas destino.
4. Indique moneda y si los valores se comparan antes o después de impuestos.
5. Especifique el importe de cada porción y su saldo; incluya cantidades solo cuando sean demostrables.
6. Adjunte el sustento de diferencias y la autorización que corresponda.
7. Solicite la validación y el registro de la aplicación conservando ambos extremos originales.

Ejemplo conceptual: de una entrega de **100,000**, una asignación válida de **30,000** deja **70,000** pendientes de asignación. Este ejemplo explica el saldo esperado; no acredita que el asistente completo esté disponible o que la prueba se haya ejecutado.

### Antecedentes y correcciones

Las aplicaciones históricas conservadas mantienen su consumo como antecedentes por conciliar. No las repita, elimine ni libere para ajustar visualmente un porcentaje.

Una devolución, corrección de factura o cambio de contrato puede afectar una aplicación. Contratos y contabilidad deben revisar sus dependencias antes de revertir o reasignar. La corrección administrativa no sustituye el retorno de mercancía ni el reverso de dinero.

<a id="cuentas"></a>
## 13. Facturas, cobros y cuentas abiertas

### Documentos del proveedor y CxP

Abra **Pagos → Facturas de proveedor** o los documentos vinculados a la compra. Antes de confirmar un documento, revise emisor, receptor, folio externo, fecha, moneda, conceptos, importes, impuestos y vencimiento, y adjunte el original.

Busque el identificador del documento antes de registrarlo desde otra orden. Si cubre varias compras, contabilidad debe verificar la distribución y evitar reconocer varias veces la misma deuda.

Consulte **Pagos → Cuentas por pagar consolidadas** por empresa y proveedor. La orden y la solicitud de pago sirven para seguimiento; no se agregan al saldo de la factura como otras deudas por el mismo hecho.

### Crear un borrador de factura desde una remisión

1. Abra la remisión entregada o firmada y revise primero si ya tiene una factura vinculada.
2. Si corresponde una nueva factura ordinaria y la remisión no tiene máscaras, contabilidad usa **Facturar**.
3. Abra el borrador generado y revise cliente, empresa, moneda, artículos, unidades, precios, impuestos y vencimiento.
4. Compare contra el documento económico real y complete la revisión antes de confirmar.

**Revise expresamente los impuestos del borrador:** la captura nueva de impuestos en la remisión no está completa en pantalla. La acción no garantiza que el borrador ya refleje toda la configuración fiscal de la operación.

Aunque una acción se llame **Facturar remisiones agrupadas**, la implementación actual genera documentos por remisión. No presuponga que una selección múltiple produce una sola factura.

Si hay máscaras, **Facturar** bloquea la generación automática y requiere trabajar con el documento económico original en contabilidad. No elimine las máscaras para evitar ese control.

### Consultar documentos y registrar cobros

Use **Cobranza → Facturas de cliente** para consultar los documentos de venta y **Cuentas por cobrar** para los saldos. Registrar un documento externo no significa emitirlo o timbrarlo automáticamente desde esta aplicación.

En una factura o documento de proveedor, la acción nativa **Pagar / Registrar pago** permite indicar diario, fecha, medio e importe. Para un parcial, registre solo el importe real y conserve el saldo. Si el dinero ya está registrado, contabilidad debe aplicar ese registro existente. El documento puede permanecer en proceso de pago hasta su conciliación bancaria. Véase la [guía oficial de pagos de Odoo 19](https://www.odoo.com/documentation/19.0/applications/finance/accounting/payments.html).

Un ingreso anticipado conserva su origen y saldo sin aplicar hasta relacionarlo con la obligación. Una promesa del cliente se registra como gestión o nota de seguimiento, con responsable y fecha; no como dinero recibido.

### Precauciones al consultar las colas

- **Remisiones por facturar** puede incluir remisiones que ya tienen una factura vinculada porque el estado físico permanece entregado o firmado. Abra el vínculo antes de generar otro documento.
- Las listas de CxP y CxC usan filtros de documentos y estados; pueden dejar fuera documentos en proceso de pago. Revise también la lista contable general cuando concilie saldos.
- Separe empresas y monedas antes de sumar. Una cifra consolidada no autoriza compensaciones entre razones sociales.
- Notas de crédito, ajustes y reembolsos requieren revisar cada documento y su aplicación. Una devolución física por sí sola no resuelve el saldo económico.

<a id="empresas"></a>
## 14. Operaciones entre empresas

Antes de registrar una operación, identifique quién compra, quién es propietario, quién custodia el material, quién vende y quién paga o cobra.

Cualquiera de las empresas habilitadas puede comprar con sus permisos y sustento. Si la pantalla solicita un motivo por usar una compradora diferente de la predeterminada, registre el motivo real. No cambie la empresa por razones de formato.

Las tres empresas del proyecto están identificadas con los datos proporcionados el 6 de septiembre de 2026:

| Nombre corto | Razón social | RFC | Domicilio fiscal |
|---|---|---|---|
| SEB Zacatecas | SERVICIOS Y EQUIPOS EN BIOTECNOLOGIA DE ZACATECAS | SEB150217A8A | Calle Llano de la Isabelica #3000, Interior 0, Fracc. Lomas de la Isabelica, C.P. 98099, Zacatecas, Zacatecas. |
| VALMA | INGENIERIA EN EQUIPOS MEDICOS VALMA | IEM1809192W9 | Calle Celso Cepeda #5029, Col. Plutarco Elías Calles, C.P. 64108, Monterrey, Nuevo León. |
| PRO OMNIMEDIC | PRO OMNIMEDIC | POM210831IH5 | Av. Ignacio Zaragoza #730, Interior 9, Col. Valle de las Trojes, C.P. 20115, Aguascalientes, Aguascalientes. |

Las tres tienen régimen de capital **Sociedad Anónima de Capital Variable** y régimen fiscal **General de Ley Personas Morales (601)**. La razón social conserva la escritura fiscal proporcionada, separada del régimen de capital. El nombre comercial completo de SEB incluye “, S.A. DE C.V.”.

**Biotex no es una empresa del proyecto.** Las denominaciones anteriores Balma y Pro fueron corregidas en las mismas fichas; los documentos conservan su empresa y sus relaciones. Para consultar o corregir los datos fiscales, abra **Ajustes → Usuarios y empresas → Empresas**, con permisos de administración. Seleccione siempre la empresa correcta antes de emitir documentos.

Las actividades declaradas difieren entre empresas. Sus porcentajes describen la constancia y no fijan límites automáticos de compra, venta o crédito. RFC, domicilio, cuentas y documentos pertenecen a cada razón social. Los datos de contacto o cuentas que no se hayan validado requieren revisión de administración.

**Inventario → Configuración → Delegaciones** corresponde al registro histórico de almacenes. **Delegaciones comerciales** permite registrar una entidad comercial diferenciada, incluso sin almacén. La configuración de ciertos vínculos con almacenes y usuarios todavía requiere apoyo de soporte.

Los menús **Ventas internas** y **Compras internas** permiten consultar documentos relacionados. Algunas pantallas conservan avisos antiguos sobre generación automática entre empresas; esos avisos no acreditan que se haya generado o confirmado la operación.

El recorrido completo de propiedad, custodia y pagos por cuenta de otra entidad sigue pendiente de completar. Para esos casos, prepare autorización y documentos con administración. El asistente ordinario de traspasos entre almacenes de la misma empresa no representa una transferencia de propiedad entre empresas.

<a id="excepciones"></a>
## 15. Excepciones operativas

### Registrar y autorizar

1. Abra **Inventario → Excepciones operativas → Nuevo**.
2. Capture **Motivo**, empresa y tipo de excepción.
3. Describa **Efecto permitido y límites**: qué se autoriza, para qué operación y hasta dónde.
4. Indique vigencia cuando corresponda y adjunte evidencia original.
5. Guarde el borrador.
6. Dirección revisa el caso y utiliza **Autorizar**. El registro conserva responsable y fecha.

Los tipos disponibles cubren regularización, sustitución, operación entre empresas, exceso, cierre, inventario y documentación.

Una excepción aprobada puede **Revocarse** conservando el antecedente. Revocar no revierte por sí mismo los hechos ya ejecutados; deben revisarse sus efectos.

La autorización necesita vincularse a la operación que la utiliza. Como ese campo todavía falta en algunos formularios, conserve ambos folios y solicite completar el vínculo con soporte. Tener una excepción aprobada no sustituye el documento del cliente o proveedor ni demuestra que hubo entrega o dinero.

<a id="indicadores"></a>
## 16. Tableros y lectura de saldos

### Consultar pendientes

Abra **Solicitudes → Tablero** o **Compras → Informes → Tablero de operación**, según sus permisos. Dirección también dispone del tablero de contratos.

Las colas ayudan a localizar solicitudes por autorizar o identificar, cotizaciones, pagos pendientes, embarques, remisiones sin firma y tareas de catálogo. Entre al documento para resolver la causa; el color o porcentaje del tablero no confirma el evento.

Algunos indicadores usan umbrales fijos heredados. Trátelos como referencias visuales mientras se validan los parámetros de la empresa. El indicador rotulado «Precio pagado» se basa en precios de compra y no demuestra un pago ejecutado.

### Interpretar importes

| Concepto | Lectura de negocio |
|---|---|
| Entrega neta | Entregas físicas confirmadas menos devoluciones relacionadas, con su valor comercial. |
| Entregado por documentar | Parte de la entrega neta sin cobertura documental válida. |
| Documentado por entregar | Compromiso físico pendiente respaldado por un documento anticipado. |
| CxC pendiente | Saldo de documentos vigentes después de notas, ajustes y cobros aplicados. |
| CxP pendiente | Saldo de obligaciones vigentes después de notas, ajustes y pagos aplicados. |
| Anticipo sin aplicar | Dinero registrado todavía pendiente de relacionarse con una obligación. |
| Avance administrativo | Aplicaciones documentadas al contrato; requiere distinguirlo del avance físico. |
| Costo | Valor de mercancía real y gastos asignados; no equivale al precio de venta. |

Estas definiciones orientan la revisión. No todos los indicadores disponen todavía de un reporte completo e independiente en la interfaz.

**Ejemplo, misma moneda y base, sin otros ajustes:** entregas por **100,000**, documentos por **70,000** que cubren parte de esas entregas y cobros aplicados por **20,000** dejan **30,000 por documentar** y **50,000 de CxC**. Los 100,000 de remisiones no se suman como otra cuenta por cobrar.

Para presentar un saldo, indique empresa, moneda, fecha de corte y si incluye impuestos. Conserve el detalle de documentos y aplicaciones que lo explica.

<a id="correcciones"></a>
## 17. Correcciones y problemas frecuentes

### Corregir conservando el historial

Un borrador sin efectos puede corregirse dentro de lo permitido por la pantalla. Para una operación confirmada, identifique qué ocurrió y quién debe resolver cada dimensión:

| Situación | Responsable y tratamiento |
|---|---|
| Necesidad reducida | Coordinación y compras revisan el saldo pendiente y los suministros relacionados. |
| Compra ya recibida | Compras y almacén revisan devolución, reposición o cierre del saldo. |
| Dinero equivocado o devuelto | Administración y contabilidad corrigen el pago y sus aplicaciones conservando el antecedente. |
| Entrega rechazada o devuelta | Almacén registra el retorno real; ventas y contabilidad revisan su efecto comercial y económico. |
| Factura o nota incorrecta | Contabilidad gestiona el documento de corrección y su saldo. |
| Aplicación contractual equivocada | Contratos revisa documentos dependientes y la reversión o reasignación sustentada. |
| Clasificación incorrecta | Catálogo revisa la ficha, sus equivalencias y documentos emitidos. |

Conserve folio original, motivo, evidencia, responsable y folios de corrección. No elimine un confirmado ni use un retroceso de estado para ocultar movimientos.

### Mensajes o comportamientos habituales

| Lo que observa | Qué revisar y cómo continuar |
|---|---|
| No aparece un menú o no puede validar inventario | Empresa activa, filtros y permisos de función; administración revisa el acceso. |
| No encuentra un documento | Quite el filtro de pendientes, propios o estado y búsquelo por folio antes de recrearlo. |
| Pide definir el importe aprobado | Capture **Importe aprobado** mientras la solicitud esté solicitada y después use **Aprobar**. |
| Advierte otras autorizaciones o pagos | Revise documentos de la misma compra y el importe ya comprometido. |
| «Un comprobante no sustituye al pago» | Revise el pago contable vinculado, su estado y el importe total solicitado. |
| Pide fecha, referencia y evidencia del pago real | Compruebe ambos registros; si falta un campo en el formulario contable, solicite completar la captura. |
| Pide motivo de cancelación, pero no aparece dónde escribirlo | Registre la incidencia con el folio y solicite soporte para la captura pendiente. |
| No permite editar una línea autorizada | La autorización protege sus datos; gestione la corrección documentada con coordinación. |
| No aparece **Cotizar / ordenar** para un saldo | Compras y soporte deben continuar el abastecimiento del saldo de la solicitud original. |
| **Activar** pide referencia externa | Complete el expediente contractual con soporte; ese campo falta en el formulario. |
| **Marcar entregada** abre Inventario | El movimiento físico aún necesita revisión y validación de almacén. |
| La impresión muestra más de lo despachado | Revise el parcial y sus pendientes antes de emitir el documento como entrega completa. |
| **Facturar** bloquea una remisión con máscaras | Contabilidad debe trabajar con el documento original y contratos con su correspondencia. |
| No permite **Reabrir / Volver a borrador** | El registro tiene antecedentes protegidos; utilice una corrección relacionada. |

Si el mensaje no coincide con el caso real, conserve la pantalla, el folio y los documentos vinculados. No intente corregirlo cambiando de empresa, inventando un dato o repitiendo la operación.

<a id="pendientes"></a>
## 18. Funciones pendientes de completar en pantalla

Esta tabla evita confundir un botón visible con un recorrido ya terminado. Los procedimientos que requieren soporte deben conservar el expediente original mientras se completa su captura.

| Área | Límite de la versión actual | Tratamiento operativo |
|---|---|---|
| Catálogo | Estados técnicos independientes y requisitos por familia incompletos. | Validar aptitud y documentos con el responsable; no interpretar **Completo** como certificación. |
| Catálogo e impresión | Algunas impresiones usan datos actuales del producto. | Conservar PDF y equivalencias históricas al reclasificar. |
| Solicitudes | Faltan campos de aclaración y ciertos vínculos de destino/delegación; algunos botones desaparecen tras el primer suministro. | Preparar notas y folios; completar la relación y el saldo con soporte. |
| Pagos | Dos acciones con el mismo nombre; referencias y cancelación con captura incompleta. | Distinguir registro de dinero y cierre; resolver los campos faltantes antes de confirmar. |
| Pagos parciales | Falta recorrido completo para ampliar una autorización ya aprobada. | Revisar el saldo con administración y documentar la ampliación. |
| Contratos | Referencia externa requerida sin campo visible; hospitales, partidas y ampliaciones sin captura completa. | Preparar borrador y expediente; activar o modificar con revisión y soporte. |
| Remisiones | Parciales pueden conservar cantidades originales en el formato. | Conciliar el documento con la salida efectiva antes de presentarlo como entrega completa. |
| Entregas especiales | Faltan vínculos visibles para entrega directa y regularización. | Resolver la ruta o excepción antes de confirmar. |
| Máscaras | Faltan campos y acciones del ciclo de aplicación, soporte y reversión. | Preparar expediente y conservar consumos históricos hasta su conciliación. |
| Facturación | Impuestos de remisión sin captura completa; selección agrupada genera documentos separados. | Revisar cada borrador y la configuración fiscal con contabilidad. |
| Devoluciones | El seguimiento integral de aplicaciones afectadas requiere intervención del responsable. | Avisar a contratos y contabilidad además de registrar el movimiento físico. |
| Entre empresas | Propiedad, custodia, pagos por cuenta ajena y sus relaciones no tienen recorrido completo. | Revisar el caso y documentos con administración; no usar un traspaso ficticio. |
| Reportes | Filtros, rótulos y umbrales antiguos pueden no expresar toda la dimensión del saldo. | Conciliar contra documentos y movimientos por empresa, moneda y corte. |

<a id="rutina"></a>
## 19. Rutina de trabajo y ejemplos

### Revisión diaria sugerida

| Responsable | Qué atender |
|---|---|
| Delegación / ventas | Necesidades pendientes, fechas requeridas, destinos y remisiones sin evidencia. |
| Coordinación | Solicitudes por autorizar, aclaraciones y cambios de necesidad. |
| Compras | Saldos por abastecer, ofertas, órdenes abiertas, rechazos y guías. |
| Almacén | Recepciones y salidas pendientes, lotes, cantidades en tránsito e incidencias. |
| Administración | Autorizaciones, beneficiarios, pagos en proceso y dinero sin aplicar. |
| Contabilidad | Documentos duplicados o pendientes, vencimientos, aplicaciones y diferencias. |
| Contratos / dirección | Expedientes, vigencias, consumo sustentado, excepciones y regularización. |

Al terminar una operación, conserve los folios relacionados y confirme qué permanece pendiente. Una revisión diaria no reemplaza el corte o conciliación formal que defina la empresa.

### Ejemplo A: compra a crédito con recepción parcial

1. Delegación solicita diez unidades del producto identificado.
2. Coordinación autoriza y compras confirma la orden por diez a crédito.
3. Almacén recibe seis y valida seis con sus lotes reales.
4. Las cuatro restantes siguen pendientes de suministro.
5. Administración registra el documento y vencimiento que correspondan; el pago se atiende en su fecha.

La recepción de seis no demuestra pago ni completa las diez unidades.

### Ejemplo B: anticipo y aplicación posterior

1. Administración autoriza un anticipo y registra la salida real con evidencia.
2. Contabilidad conserva ese dinero identificado como pendiente de aplicación.
3. Al llegar el documento definitivo, aplica el anticipo existente.
4. Revisa el saldo restante del documento y del anticipo.

La aplicación no genera otra transferencia ni otra salida de dinero.

### Ejemplo C: entrega ordinaria y cobro parcial

1. Ventas prepara una remisión con los productos y cantidades que efectivamente se entregarán.
2. Almacén valida la salida y registra el estado entregada; ventas recaba la evidencia disponible.
3. Contabilidad revisa y confirma el documento económico correspondiente.
4. Administración registra el ingreso parcial real y contabilidad verifica su aplicación.
5. Se conserva el saldo de la factura hasta que se cubra o ajuste con soporte.

La firma no confirma el cobro y el cobro no sustituye la entrega.

Estos recorridos son ejemplos de capacitación. Practíquelos en una instancia de pruebas autorizada y registre los resultados; no cree operaciones ficticias en la base operativa.

<a id="soporte"></a>
## 20. Glosario, soporte y referencia de versión

### Glosario

| Término | Significado |
|---|---|
| Folio | Referencia visible de un documento para localizarlo y relacionarlo. |
| RFQ | Solicitud de presupuesto enviada o preparada para un proveedor. |
| OC | Orden de compra confirmada como compromiso de suministro. |
| Delegación comercial | Sede o ámbito de atención comercial; puede operar sin almacén propio. |
| Almacén / ubicación | Lugar físico o ubicación lógica utilizada para controlar mercancía. |
| Propietario | Entidad a la que pertenece el material. |
| Custodia | Responsabilidad física sobre el material, aunque pertenezca a otra entidad. |
| Remisión | Documento operativo de los artículos incluidos en una entrega. |
| Máscara | Correspondencia administrativa sustentada entre entrega, contrato y documento. |
| Aplicación | Relación de una porción de dinero o valor con un documento; su efecto depende del tipo de aplicación. |
| CxP / CxC | Cuentas por pagar / cuentas por cobrar. |
| Regularización | Asignación documentada posterior de una operación que conservaba ese pendiente. |
| Reverso | Corrección relacionada que conserva el antecedente y explica el efecto revertido. |

### Reportar una incidencia

Envíe por el canal de soporte acordado:

- Usuario, empresa activa y área responsable.
- Fecha y hora del caso.
- Menú, folio y documento relacionado.
- Acción realizada y mensaje exacto.
- Resultado esperado y resultado observado.
- Cantidades o importes afectados, con moneda y base cuando corresponda.
- Evidencia pertinente y referencia de la regla de negocio, si se conoce.

No incluya contraseñas ni datos bancarios innecesarios. El responsable debe poder identificar el caso sin repetir el movimiento para reproducirlo.

### Base documental y mantenimiento

La referencia de esta guía son las vistas y acciones de los módulos existentes de catálogo, solicitudes, compras, pagos, contratos, remisiones, operación entre empresas y experiencia de usuario. La [evidencia de actualización del 5 de septiembre de 2026](evidence/deployment-20260905.md) identifica las versiones y los commits correspondientes.

Las reglas de negocio proporcionadas por la empresa sirven para explicar el significado esperado de hechos, saldos y excepciones. Los pendientes descritos aquí deben actualizarse cuando sus pantallas y recorridos se completen y prueben.

La comprobación técnica de la actualización y conservación de datos es distinta de la aceptación funcional de cada proceso. Para esta última, cada responsable debe ejecutar sus casos autorizados, registrar folios, resultados y evidencia y confirmar los parámetros de su área.
