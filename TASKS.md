# Tareas — marca + probador

## Parte 1 — Identidad de marca
- [x] `marca.toml` ampliado desde la carpeta de marketing (público, tono, evitar, contacto, colores, tipografías)
- [x] Logo y tipografías en `app/static/` (Inter y Cormorant Garamond, licencia OFL)
- [x] Página `/marca` detrás de la clave
- [x] Toda la app usa la identidad (colores desde `marca.toml`, modo claro y oscuro)
- [ ] `marca/PENDIENTE.md` con lo que la carpeta no define (ver abajo)

Pendiente de definir por los dueños (no está en la carpeta de marketing):
- No hay manual de marca oficial: los colores salen del logo de Instagram.
- Edad y perfil de las clientas: sin datos.
- Condiciones para clientas nuevas (momento del pago, cambios, reserva de stock).
- Transportadora, tarifa de envío y quién la paga.

No se copió al repo: videos y colecciones de la carpeta de marketing (8,1 GB).

## Parte 2 — Probador virtual con IA
- [x] FLUX.2 [pro] desplegado en `ai-indigo-5dvav` (Brazil South); la app entra con su identidad, sin API key
- [x] Página pública `/probador`: modelo de ejemplo + prendas; al tocar una prenda se genera la foto
- [x] Modelo y 4 prendas de ejemplo generadas con IA y cargadas en Blob (`probador/`)
- [x] Foto propia con aviso y aceptación; no se guarda; se le quitan los metadatos
- [x] Topes por día y por persona guardados en Blob; interruptor `PROBADOR_IA=0`
- [x] Página privada `/probador/prendas`: subir y borrar prendas, cambiar la modelo, ver el uso del día
- [x] Tests: 36 pasan (con FLUX y Azure de mentira)
- [ ] Revisar el costo real por foto en Cost Management después de unos días de uso
- [ ] Probar con fotos reales de clientas y de prendas de la tienda, y ajustar la instrucción si hace falta

Decisiones:
- Se descartó la primera versión (prenda dibujada encima de la foto) por poco realista.
- No hay tope "por sesión": se controla por persona (IP) y por día, que es lo que protege el gasto.
