# Tomas para los videos plantilla

Acá se dejan los clips que se graban. El motor los detecta solo: cuando está el archivo de una toma, reemplaza al cartel "FALTA GRABAR" de ese lugar.

## Cómo nombrar cada clip

- El nombre es el número del video, guion bajo, `toma` y el número de toma. Ejemplo: `07_toma1.mp4`, `19_toma3.mov`.
- Sirve `.mp4` o `.mov` (da igual si va en mayúsculas). Si hay de los dos, se usa el `.mp4`.
- Un clip por toma. Si grabaste varias veces, dejá solo la mejor con el nombre correcto.

## Cómo grabar

- En vertical (celular parado), con el sujeto en el centro: el motor recorta al centro a formato vertical 9:16.
- Sin tapar el centro con la mano. Sin datos personales a la vista (direcciones, teléfonos, nombres de clientas).
- El sonido del clip no se usa: el video lleva la música. Si querés que se escuche tu voz, eso se agrega después en la app de edición.
- Duración: grabá **al menos** la duración mínima de la tabla (mejor 1 segundo más, y el motor corta lo que sobra). Si el clip es más corto, el motor lo usa entero, deja quieto el último cuadro y **te avisa** cuántos segundos faltaron.

## Qué pasa al armar los videos

- Con una toma sola, el video sigue siendo plantilla: el aviso dice el nombre exacto del archivo que falta.
- Un video se arma como final solo cuando están **todas** sus tomas y **todos** sus datos (alturas, talles, nombre, etc. en `motor/datos.json`).
- Para ver qué falta: `python3 motor/lote.py --dias 7 --plan` y mirar `datos-faltantes.md`.

## Lista de tomas

La duración mínima es la del tramo real dentro del video (redondeada a medio segundo); puede ser distinta de la que dice el cartel.

### Video 07 · Altura y talle

| Archivo | Qué grabar | Mínimo |
|---|---|---|
| `07_toma1.mp4` | Plano de perfil: cintura y cadera: Plano medio, 3 s, luz de costado; Y una caminata hacia cámara, 2 s; Completar altura y talle reales | 2,5 s |

### Video 10 · Mismo jean, dos cuerpos

| Archivo | Qué grabar | Mínimo |
|---|---|---|
| `10_toma1.mp4` | Mismo jean, dos cuerpos: Una segunda persona con el mismo jean; Mismo encuadre fijo, frente y perfil; 2 tomas cada una y 1 juntas | 3,0 s |

### Video 11 · Caminar, sentarse, agacharse

| Archivo | Qué grabar | Mínimo |
|---|---|---|
| `11_toma1.mp4` | Gancho: cuclillas de golpe: Plano de perfil, 2 s, 2 tomas | 2,0 s |
| `11_toma2.mp4` | Faltan: sentada y escalón: Sentada en plano medio, cruza la pierna; Sube un escalón, 2 s cada una | 2,0 s |

### Video 12 · Tiro alto de verdad

| Archivo | Qué grabar | Mínimo |
|---|---|---|
| `12_toma1.mp4` | Dedo marcando la pretina: Detalle de cintura, frente y perfil; 2 tomas de 3 s | 2,0 s |

### Video 19 · Así preparamos tu pedido

| Archivo | Qué grabar | Mínimo |
|---|---|---|
| `19_toma1.mp4` | Así preparamos tu pedido: Cenital sobre una mesa, luz de ventana; 5 planos de 3 s con sonido real; Sin datos personales a la vista | 3,0 s |
| `19_toma2.mp4` | Doblamos: Manos doblan la prenda | 2,5 s |
| `19_toma3.mp4` | Envolvemos: Papel o bolsa, a 1,5× | 2,5 s |
| `19_toma4.mp4` | Tu nombre: Nota a mano, sin dirección | 2,5 s |
| `19_toma5.mp4` | Listo para enviar: Paquete cerrado en la mano | 2,5 s |

### Video 21 · Elegimos prenda por prenda

| Archivo | Qué grabar | Mínimo |
|---|---|---|
| `21_toma1.mp4` | Mano recorriendo perchas: Punto de vista, 2 s, a 1,5×; Es el gancho del video | 2,0 s |

### Video 22 · Quién te responde

| Archivo | Qué grabar | Mínimo |
|---|---|---|
| `22_toma1.mp4` | Quién te responde los mensajes: Hablado a cámara, plano medio; Ventana de frente, perchero de fondo; 18 s con el guion del documento | 3,0 s |
| `22_toma2.mp4` | Hola, soy (nombre).: Subtítulo en pantalla | 2,5 s |
| `22_toma3.mp4` | Soy la que te responde.: Subtítulo en pantalla | 2,5 s |
| `22_toma4.mp4` | Elegimos, te asesoramos y enviamos.: Subtítulo en pantalla | 2,5 s |
| `22_toma5.mp4` | Escribime. Te respondo yo.: Subtítulo en pantalla | 2,5 s |

### Video 24 · La pila entera primero

| Archivo | Qué grabar | Mínimo |
|---|---|---|
| `24_toma1.mp4` | La pila entera primero: Plano medio con la pila en brazos; 6 prendas, 1,5 s cada una; Cada una tapa el lente al desplegarse | 2,5 s |

## Cosas a saber

- Videos 19 y 22: la primera toma (`toma1`) es el cartel general; las siguientes (`toma2` a `toma5`) son las que el cartel llama "TOMA 1" a "TOMA 4" (video 19) o "VOZ" (video 22).
- Video 22, tomas `toma2` a `toma5`: el cartel trae el texto exacto del subtítulo y el video lo muestra solo, sobre el clip.
- Video 22, `toma1` (el gancho hablado): el cartel solo dice que hay que hablar a cámara con el guion del documento. No se pone texto: si hace falta un subtítulo, se agrega después en la app de edición.
- Video 28 no necesita tomas: solo los datos (prenda, unidades, talles). Con los tres cargados en `datos.json`, el cartel "FALTA COMPLETAR" desaparece y el video queda listo (y más corto, porque el cartel ocupaba 4 tiempos).
- Para probar con otra carpeta: `python3 motor/lote.py --dias 7 --tomas ruta/a/otra/carpeta`. Una carpeta con un archivo `EJEMPLO.txt` se considera de prueba: todo lo que se arme con ella sale marcado `_EJEMPLO` (no publicar).
