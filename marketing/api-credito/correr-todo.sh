#!/bin/bash
# Un solo comando: pide la key si falta, muestra el costo, pide confirmacion y manda los 3 lotes.
# Uso:  bash ~/vibe_coding/indigo-py-marketing/api-credito/correr-todo.sh
cd "$(dirname "$0")" || exit 1
K="$HOME/.config/indigo/api_key"
if [ -z "$ANTHROPIC_API_KEY" ] && [ ! -s "$K" ]; then
  mkdir -p "$HOME/.config/indigo"
  read -s -p "Pega tu API key (no se ve al escribir) y apreta Enter: " k; echo
  printf %s "$k" > "$K"; chmod 600 "$K"; unset k
  echo "Key guardada en tu Mac."
fi
echo; echo "== Costo maximo estimado =="
python3 indigo_api.py plan todas || exit 1
echo; read -p "Mandar los lotes de catalogo, contenido y dms? (s/n) " r
[ "$r" = "s" ] || { echo "Cancelado, no se gasto nada."; exit 0; }
for t in catalogo contenido dms; do
  if [ -f "salida/$t/batch.json" ]; then echo "$t: ya estaba enviado, lo salteo"; continue; fi
  python3 indigo_api.py enviar "$t" || echo "$t: NO se envio (mira el mensaje de arriba)"
done
echo; echo "== Estado =="
python3 indigo_api.py estado todas
echo; echo "Listo. Para ver como va:  python3 indigo_api.py estado todas"
