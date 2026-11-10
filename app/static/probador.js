// Probador: le pide al servidor una foto de la persona con la prenda puesta.
// Con la modelo de ejemplo no se envía ninguna foto. Con la foto de la clienta, se envía
// solo después de que acepta el aviso, y el servidor no la guarda.
(() => {
  const $ = (id) => document.getElementById(id);
  const datos = JSON.parse($("datos").textContent);
  const prendaPorId = Object.fromEntries(datos.prendas.map((p) => [p.id, p]));
  const ORDEN = ["arriba", "entera", "abajo"];
  const persona = $("persona");
  const fotoModelo = persona.src;

  const elegidas = new Map(); // tipo -> id
  const hechas = new Map(); // "id,id" -> URL del resultado, para la persona actual
  let miFoto = null; // la foto de la clienta, ya achicada (o null si usa la modelo)
  let miFotoUrl = null;
  let acepto = false;
  let ocupado = false;

  const clave = () => ORDEN.map((t) => elegidas.get(t)).filter(Boolean).join(",");
  const base = () => miFotoUrl || fotoModelo;

  function refrescar() {
    const puestas = new Set(elegidas.values());
    for (const boton of document.querySelectorAll(".prenda")) {
      boton.setAttribute("aria-pressed", puestas.has(boton.dataset.id));
      boton.disabled = ocupado || !datos.activo;
    }
    $("usar-foto").disabled = ocupado || !datos.activo;
    $("quitar").hidden = puestas.size === 0 || ocupado;
    $("usar-modelo").hidden = !miFoto || ocupado;
    $("velo").hidden = !ocupado;

    // El mensaje de WhatsApp nombra solo prendas reales de la tienda, nunca las de ejemplo.
    const nombres = [...puestas].map((id) => prendaPorId[id]).filter((p) => !p.ejemplo).map((p) => p.nombre);
    const texto = nombres.length
      ? `Hola ${datos.marca}, me probé en el probador: ${nombres.join(" y ")}. ¿Me pasan precio y talles?`
      : `Hola ${datos.marca}, estuve mirando el probador. ¿Me cuentan qué tienen disponible?`;
    $("la-quiero").href = `${datos.whatsapp}?text=${encodeURIComponent(texto)}`;
    $("la-quiero").textContent = nombres.length ? "La quiero: consultar por WhatsApp" : "Consultar por WhatsApp";
  }

  function ver(url, generada) {
    persona.src = url;
    $("leyenda").hidden = !generada;
  }

  function avisar(texto) {
    $("mensaje").textContent = texto || "";
    $("mensaje").hidden = !texto;
  }

  async function probar() {
    const pedido = clave();
    avisar("");
    if (!pedido) return ver(base(), false);
    if (hechas.has(pedido)) return ver(hechas.get(pedido), true);

    ocupado = true;
    refrescar();
    const cuerpo = new FormData();
    cuerpo.append("prendas", pedido);
    if (miFoto) {
      cuerpo.append("acepto", "si");
      cuerpo.append("foto", miFoto, "foto.jpg");
    }
    try {
      const r = await fetch("/probador/probar", { method: "POST", body: cuerpo });
      if (!r.ok) {
        const fallo = await r.json().catch(() => ({}));
        throw new Error(fallo.error || "No se pudo generar la imagen. Probá de nuevo.");
      }
      const url = URL.createObjectURL(await r.blob());
      hechas.set(pedido, url);
      ver(url, true);
    } catch (e) {
      elegidas.clear();
      ver(base(), false);
      avisar(e.message);
    } finally {
      ocupado = false;
      refrescar();
    }
  }

  function cambiarPersona(foto) {
    for (const url of hechas.values()) URL.revokeObjectURL(url);
    hechas.clear();
    elegidas.clear();
    if (miFotoUrl) URL.revokeObjectURL(miFotoUrl);
    miFoto = foto;
    miFotoUrl = foto ? URL.createObjectURL(foto) : null;
    persona.alt = foto ? "Tu foto" : "Modelo de ejemplo";
    avisar("");
    ver(base(), false);
    refrescar();
  }

  // Achica la foto en el teléfono antes de enviarla: sube más rápido y gasta menos datos.
  async function achicar(archivo) {
    try {
      const imagen = await createImageBitmap(archivo);
      const escala = Math.min(1, 1280 / Math.max(imagen.width, imagen.height));
      const lienzo = document.createElement("canvas");
      lienzo.width = Math.round(imagen.width * escala);
      lienzo.height = Math.round(imagen.height * escala);
      lienzo.getContext("2d").drawImage(imagen, 0, 0, lienzo.width, lienzo.height);
      return await new Promise((listo) => lienzo.toBlob((b) => listo(b || archivo), "image/jpeg", 0.88));
    } catch {
      return archivo; // si el navegador no la puede leer, va como está y decide el servidor
    }
  }

  $("percha").addEventListener("click", (e) => {
    const boton = e.target.closest(".prenda");
    if (!boton || ocupado || !datos.activo) return;
    const { id, tipo } = prendaPorId[boton.dataset.id];
    if (elegidas.get(tipo) === id) {
      elegidas.delete(tipo);
    } else {
      // Una prenda por lugar; una prenda entera reemplaza a la de arriba y a la de abajo.
      if (tipo === "entera") elegidas.clear();
      else elegidas.delete("entera");
      elegidas.set(tipo, id);
    }
    refrescar();
    probar();
  });

  $("quitar").addEventListener("click", () => {
    elegidas.clear();
    refrescar();
    probar();
  });

  $("usar-foto").addEventListener("click", () => (acepto ? $("mi-foto").click() : $("aviso").showModal()));
  $("no-acepto").addEventListener("click", () => $("aviso").close());
  $("acepto").addEventListener("click", () => {
    acepto = true;
    $("aviso").close();
    $("mi-foto").click();
  });
  $("mi-foto").addEventListener("change", async (e) => {
    const archivo = e.target.files[0];
    e.target.value = "";
    if (archivo) cambiarPersona(await achicar(archivo));
  });
  $("usar-modelo").addEventListener("click", () => cambiarPersona(null));

  refrescar();
})();
