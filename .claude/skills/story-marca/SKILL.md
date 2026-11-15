---
name: story-marca
description: Stories de marca sin prenda (1080x1920) para Índigo Py, con colores de marca.toml, logo, Inter y Cormorant, botón "Pedí por WhatsApp" y código de pieza.
---

# Stories de marca

1. Armá un JSON (guardalo como `docs/campanas/<semana>/marca/piezas.json`, junto a los PNG) con la lista de piezas: `archivo`, `etiqueta`, `titulo`, `cuerpo` (usá \n para separar párrafos), `codigo` y, si lleva sticker de preguntas, `hueco_sticker: true` (texto corto, para que quede espacio libre en el medio).
2. `python3 .claude/skills/story-marca/hacer_stories.py docs/campanas/<semana>/marca piezas.json`
3. Mirá todas juntas en una hoja de contacto achicada a 540 px de ancho: si no se lee a ese tamaño, no se lee en el celular.
4. Textos: solo datos de marca.toml (WhatsApp, transferencia, envíos a todo Paraguay por transportadora). Precio, talle, plazo o costo de envío: "consultá por WhatsApp".
5. Nunca dibujes avisos tipo "(acá va el sticker)" dentro de la imagen: se publicarían.
6. Zonas seguras: nada importante arriba de y=230 ni abajo de y=1750.
7. Si la story va también al estado de WhatsApp: la misma imagen, texto con "Respondé este estado" y el mismo código. No hay sticker de enlace ni de preguntas.
