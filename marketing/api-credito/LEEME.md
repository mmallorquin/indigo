# Indigo PY · trabajos con la API (crédito que vence 15/11, 21:00 hora de Paraguay)

Todo corre **en tu Mac, desde la Terminal**, para que la API key nunca salga de tu computadora.

## 1. Guardar la key (una sola vez)

Abrí Terminal y pegá esto. Te va a pedir la key y NO la muestra al escribir:

```
mkdir -p ~/.config/indigo && read -s -p "API key: " k && printf %s "$k" > ~/.config/indigo/api_key && chmod 600 ~/.config/indigo/api_key && unset k && echo OK
```

La key tiene que ser de la organización que tiene el crédito (Console → API keys). Ponele un límite de gasto en Console.

## 2. Ver cuánto costaría (no gasta nada)

```
cd ~/vibe_coding/indigo/marketing/api-credito
python3 indigo_api.py plan todas
```

## 3. Enviar los lotes (Batch = mitad de precio, pueden tardar hasta 24 h)

```
python3 indigo_api.py enviar catalogo
python3 indigo_api.py enviar contenido
python3 indigo_api.py enviar dms
python3 indigo_api.py estado todas        # repetir cada tanto
python3 indigo_api.py bajar contenido     # cuando diga "ended"
```

Los resultados quedan en `api-credito/salida/<tarea>/`. Después, el juez (elige lo mejor):

```
python3 indigo_api.py enviar juez --modelo opus
python3 indigo_api.py bajar juez
```

## 4. Si el tiempo aprieta: tiempo real (sin esperar al lote, precio completo)

```
python3 indigo_api.py ahora dms --modelo sonnet
```

## 5. Gasto real

```
python3 indigo_api.py gasto
```

## Reglas que el script impone al modelo
- Nunca inventa precio, talle, tela, stock, envío, pago ni fechas: deja `[FALTA: ...]`.
- Sin escasez falsa. Sin promesas de cambios o garantías (política pendiente).
- Español paraguayo con voseo.

## Notas
- Modelos: `haiku`, `sonnet` (por defecto), `opus` (`--modelo opus`).
- `--tope` corta el envío si el costo máximo estimado lo supera (por defecto US$ 15).
- Precios usados (USD por millón de tokens, entrada/salida, estándar; Batch es la mitad): Haiku 5.5 0,10/0,50 · Sonnet 5.5 2/10 · Opus 5.5 4/20. Verificar en la Console.
- Solo se leen archivos; nunca se modifica ni borra nada de tu carpeta.
