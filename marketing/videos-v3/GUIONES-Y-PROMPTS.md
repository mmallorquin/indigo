# Índigo Py — guiones y motion v3

Ruta A: combinaciones reales. Tratamiento M1: moda enérgica, con títulos breves, cambios reales de outfit y pausas que dejan ver el jean. Dos piezas de 20 segundos. La dirección índigo profundo/cobalto es una propuesta gráfica, no un manual de marca confirmado.

El material se recorta para retirar el título incrustado y conservar cabeza, cintura, largo y zapatos. No se genera ropa, persona, voz, perspectivas ni detalles. No se aplican cambios al color del jean. El movimiento de la persona proviene del video original; la cámara digital mantiene escala constante después del recorte.

## Montaje real

Los rangos se expresan en segundos del original, a 30 fps. El JSON de cada pieza conserva los cuadros exactos. Intervalos con fin exclusivo.

| Tramo | Reel looks | Reel consulta |
|---|---|---|
| Primer plano | 0–2,000: blazer fucsia, fuente 10,700–12,700 | 0–1,433: negro, fuente 4,167–5,600 |
| Segundo plano | 2,000–2,800: verde oscuro, fuente 1,000–1,800 | 1,433–2,233: verde oscuro, fuente 1,000–1,800 |
| Tercer plano | 2,800–4,233: negro, fuente 4,167–5,600 | 2,233–4,233: blazer fucsia, fuente 10,700–12,700 |
| Lila | 4,233–6,833: fuente 6,200–8,800 | Igual |
| Fucsia y giro | 6,833–12,200: fuente 12,200–17,567 | Igual |
| Verde claro | 12,200–14,200: fuente 18,000–20,000 | Igual |
| Abrigo beige | 14,200–17,800: fuente 21,000–24,600 | Igual |
| Cierre en movimiento | 17,800–20,000: fuente 25,500–27,700 | Igual |

Hay una reutilización de 0,5 segundos del plano fucsia en ambos montajes. Se presenta como montaje de combinaciones, sin atribuir nuevas grabaciones o nuevas prendas. Los cortes evitan las transiciones con desplazamiento vertical de la fuente.

## Motion y lectura

| Pieza / tiempo | Texto | Entrada / lectura / salida | Propósito |
|---|---|---|---|
| Looks 0,03–1,80 | UN JEAN | Revelado por palabra 0,42 s; frame entra desde x −35 y escala 0,97 en 0,32 s; salida últimos 0,20 s hacia y −22 | Mostrar producto y resolver tema rápidamente |
| Looks 1,93–4,03 | VARIOS / LOOKS | VARIOS por carácter; LOOKS desde x +45 con retraso 0,12 s; lectura estable después del revelado; salida 0,20 s | Cambio de outfit conecta el gancho con la demostración |
| Looks 6,97–8,92 | CAMBIÁ EL LOOK | Mismo sistema de 0,42 s y salida 0,20 s | Relacionar el giro real con versatilidad |
| Looks 12,25–13,95 | ¿CUÁL VA CON VOS? | Revelado 0,42 s; lectura estable; salida 0,20 s | Preparar interés y consulta |
| Consulta 0,03–2,15 | ¿BUSCÁS / JEANS? | Dos líneas animadas, segunda con retraso 0,12 s; salida 0,20 s | Identificar intención de compra |
| Consulta 4,55–6,10 | TU MODELO | Entrada 0,42 s; lectura; salida 0,20 s | Pedir necesidad concreta |
| Consulta 7,30–8,85 | TU TALLE | Entrada 0,42 s; lectura; salida 0,20 s | Orientar la consulta sin afirmar talles disponibles |
| Consulta 12,25–13,95 | TU CIUDAD | Entrada 0,42 s; lectura; salida 0,20 s | Poder evaluar entrega y cotización |
| Ambos 16–20 | ÍNDIGO PY / ESCRIBINOS / JEANS / por WhatsApp | Frame entra 0,35 s desde x −40; palabras reveladas 0,30 s con retrasos de 0; 0,13; 0,20 s. Después quedan estables hasta el fin | Un único CTA sobre producto real en movimiento |

Los títulos usan Bebas Neue y la información DM Sans. Cada palabra tiene espacio negativo real detrás; no hay banda sólida, tarjeta, botón falso ni párrafo fijo. Los trazos cobalto se expanden en 0,30 s cuando aparece un título de una línea. Los tramos sin texto permiten observar la ropa. El CTA queda arriba y a la izquierda, sin cubrir el rostro, cintura o piernas. No se publica un número en pantalla.

Música: instrumental sintetizada propia, 120 BPM, con acentos suaves en las entradas tipográficas. Los acentos cambian de momento entre piezas para seguir cada guion. El archivo original no tiene audio ni diálogo. Se entregan masters silenciosos. No hay canción de una red social ni muestras de terceros.

## Prompts de edición por toma

Aplicar este bloque común a cada intervalo de la tabla: «Usar únicamente source.mp4, CREADORA-REF-01 y JEAN-REF-01. Recortar x=100, y=232, ancho=590, alto=1048; convertir a 1080×1920 conservando la imagen real. Respetar el rango de cuadros del JSON. Corte directo al cambiar de combinación; no inventar ángulos, detalles, stock, precio, talla o experiencia de compra. Mantener la persona y el producto sin deformaciones ni recoloración. Animar gráficos nativos, nunca una captura de HTML».

- Fucsia inicial: abrir ya con la modelo y el jean; superponer el gancho correspondiente, sin presentación de logo.
- Verde oscuro y negro: cambios rápidos reales que resuelven el gancho; conservar cuerpo completo y no acelerar o interpolar los movimientos.
- Lila: mantener 2,6 segundos de demostración. En consulta, presentar TU MODELO; en looks, dejar la ropa libre de texto.
- Fucsia y giro: aprovechar el movimiento existente y mantener pausas limpias. En looks, CAMBIÁ EL LOOK; en consulta, TU TALLE. No usar el blazer para afirmar detalles de cintura o espalda que cubre.
- Verde claro: pregunta de preferencia o TU CIUDAD según pieza; dejar salir el título antes del siguiente outfit.
- Abrigo beige: empezar con imagen limpia y después incorporar el CTA. El abrigo cubre parte del jean; no atribuirle una demostración de cintura o bolsillos.
- Última toma beige: continuar el CTA legible y la imagen real hasta el fin, sin placa estática de cuatro segundos.

## Captions y ganchos alternativos

**Looks:** Un jean, varias ideas para combinarlo. ¿Cuál va con vos? Escribinos **JEANS por WhatsApp** y contanos qué modelo y talle buscás, y tu ciudad.

**Consulta:** ¿Buscás jeans? Contanos qué modelo querés, tu talle y en qué ciudad estás. Escribinos **JEANS por WhatsApp** para consultar las opciones.

Alternativas de gancho: «UN JEAN / TU ESTILO» y «¿CUÁL ELEGÍS?». Para aislar su efecto, cambiar únicamente el comienzo de una misma pieza y mantener cuerpo, CTA, distribución y ventana de medición.

Registrar consultas nuevas, consultas con necesidad/modelo, talle y ciudad; cotizaciones; pedidos pagados y entregados. Anotar qué pieza originó la consulta cuando se pueda identificarlo. Estas dos entregas cambian el gancho y parte del montaje: compararlas explora enfoques, no aísla una variable ni demuestra causalidad. No se fijan metas ni presupuesto con estos datos iniciales.

## Portadas y alternativa de diseño

Las portadas nativas usan el gancho arriba y el outfit real completo. Jerarquía: primero el título breve, después la modelo y el jean. El recorte de cuadrícula puede variar por destino; las portadas se entregan completas en 9:16.

Alternativa para una futura pieza: M3 con palabra grande entrando desde un lateral durante un cambio de outfit, saliendo por máscara en 0,25 s y dando paso a tres segundos de ropa limpia. La composición cambia a bloques tipográficos laterales breves, con el CTA en dos líneas arriba sobre el último plano. Es una dirección alternativa, no una tercera pieza exportada.

