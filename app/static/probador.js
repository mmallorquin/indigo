// Probador: la persona al centro y, debajo, una rueda de prendas que gira al deslizar.
// Ojear la rueda no llama al servidor. Solo "Fijar" y "Girar" piden una foto generada.
// Con la modelo de ejemplo no se envía ninguna foto. La foto de la clienta se envía
// solo después de que acepta el aviso, y el servidor no la guarda.
(() => {
  const $ = (id) => document.getElementById(id);
  const datos = JSON.parse($("datos").textContent);
  const prendaPorId = Object.fromEntries(datos.prendas.map((p) => [p.id, p]));
  const etiquetas = Object.fromEntries(datos.pestanas); // llega como lista de pares para conservar el orden
  const categorias = datos.pestanas.map(([t]) => t).filter((t) => datos.prendas.some((p) => p.tipo === t));
  const ORDEN = ["arriba", "entera", "abajo", "cinto", "accesorio"]; // mismo orden que usa el servidor
  const GRADOS = 17; // separación entre cartas del abanico
  const LEYENDAS = {
    frente: "Imagen generada con IA. El calce real puede variar.",
    perfil: "Vista generada con IA; la espalda puede no coincidir con la prenda real.",
    espalda: "Vista generada con IA; la espalda puede no coincidir con la prenda real.",
  };
  const persona = $("persona");
  const fotoModelo = persona.src;
  const rueda = $("rueda");

  let puesto = new Map(); // tipo -> id de la prenda fijada
  let vista = "frente";
  const hechas = new Map(); // "ids|vista" -> URL del resultado, para la persona actual
  let miFoto = null; // la foto de la clienta ya achicada, o null si usa la modelo
  let miFotoUrl = null;
  let acepto = false;
  let ocupado = false;
  let categoria = categorias[0];
  const posicion = Object.fromEntries(categorias.map((c) => [c, 0])); // qué carta está al centro en cada rueda

  const enRueda = () => datos.prendas.filter((p) => p.tipo === categoria);
  const delCentro = () => enRueda()[posicion[categoria]];
  const clave = () => ORDEN.map((t) => puesto.get(t)).filter(Boolean).join(",");
  const base = () => miFotoUrl || fotoModelo;

  // ---------- La rueda ----------

  // Distancia de cada carta al centro, dando la vuelta: con 5 cartas va de -2 a 2.
  function distancia(i, n) {
    let d = (i - posicion[categoria]) % n;
    if (d > n / 2) d -= n;
    if (d < -n / 2) d += n;
    return d;
  }

  function acomodarRueda(arrastre = 0) {
    const cartas = rueda.querySelectorAll(".carta");
    cartas.forEach((carta, i) => {
      const d = distancia(i, cartas.length) + arrastre;
      const lejos = Math.abs(d);
      carta.style.transform = `rotate(${d * GRADOS}deg) translateY(${lejos < 0.5 ? -12 : 0}px)`; // la del centro, un poco más arriba
      carta.style.opacity = lejos > 2.6 ? 0 : 1 - Math.min(lejos, 2) * 0.22;
      carta.style.zIndex = 10 - Math.round(lejos);
      carta.classList.toggle("centro", Math.round(d) === 0);
      carta.tabIndex = -1;
    });
  }

  function armarRueda() {
    rueda.querySelectorAll(".carta").forEach((c) => c.remove());
    enRueda().forEach((p, i) => {
      const carta = document.createElement("button");
      carta.type = "button";
      carta.className = "carta";
      carta.dataset.i = i;
      carta.setAttribute("aria-label", p.nombre);
      const img = document.createElement("img");
      img.src = `/probador/prenda/${p.id}.jpg`;
      img.alt = "";
      img.draggable = false;
      carta.appendChild(img);
      rueda.appendChild(carta);
    });
    const varias = enRueda().length > 1;
    $("anterior").hidden = $("siguiente").hidden = !varias;
    acomodarRueda();
  }

  function girarRueda(pasos) {
    const n = enRueda().length;
    if (n < 2) return;
    posicion[categoria] = (((posicion[categoria] + pasos) % n) + n) % n;
    acomodarRueda();
    refrescar();
  }

  function cambiarCategoria(nueva) {
    categoria = nueva;
    armarRueda();
    refrescar();
  }

  // Deslizar: la rueda acompaña al dedo y, al soltar, queda en la carta más cercana.
  if (rueda) {
    let toque = null;
    rueda.addEventListener("pointerdown", (e) => {
      if (e.target.closest(".flecha")) return;
      toque = { x: e.clientX, movido: false, carta: e.target.closest(".carta") };
      rueda.classList.add("arrastrando");
    });
    rueda.addEventListener("pointermove", (e) => {
      if (!toque) return;
      const dx = e.clientX - toque.x;
      if (Math.abs(dx) > 6) toque.movido = true;
      if (toque.movido && enRueda().length > 1) acomodarRueda(dx / 110);
    });
    const soltar = (e) => {
      if (!toque) return;
      const dx = (e.clientX ?? toque.x) - toque.x;
      const { movido, carta } = toque;
      toque = null;
      rueda.classList.remove("arrastrando");
      if (movido) girarRueda(-Math.round(dx / 110) || (Math.abs(dx) > 40 ? -Math.sign(dx) : 0));
      else if (carta) girarRueda(distancia(Number(carta.dataset.i), enRueda().length)); // tocar una vecina la trae al centro
      acomodarRueda();
    };
    rueda.addEventListener("pointerup", soltar);
    rueda.addEventListener("pointercancel", soltar);
    rueda.addEventListener("pointerleave", (e) => toque && soltar(e));
    rueda.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") girarRueda(1);
      else if (e.key === "ArrowLeft") girarRueda(-1);
      else if (e.key === "Enter" && e.target === rueda) $("fijar").click();
      else return;
      e.preventDefault();
    });
    $("anterior").addEventListener("click", () => girarRueda(-1));
    $("siguiente").addEventListener("click", () => girarRueda(1));
  }

  // ---------- Lo que se ve ----------

  function refrescar() {
    const puedeGenerar = datos.activo && !ocupado;
    const prenda = delCentro();

    // Pestañas
    const pestanas = $("pestanas");
    if (pestanas && !pestanas.children.length) {
      for (const c of categorias) {
        const b = document.createElement("button");
        b.type = "button";
        b.role = "tab";
        b.dataset.categoria = c;
        b.textContent = etiquetas[c];
        b.addEventListener("click", () => cambiarCategoria(c));
        pestanas.appendChild(b);
      }
    }
    pestanas?.querySelectorAll("button").forEach((b) => {
      b.setAttribute("aria-selected", b.dataset.categoria === categoria);
      b.classList.toggle("con-prenda", puesto.has(b.dataset.categoria));
    });

    // Carta del centro y su botón
    if (prenda) {
      const yaPuesta = puesto.get(prenda.tipo) === prenda.id;
      $("nombre").textContent = yaPuesta ? `${prenda.nombre} · ya puesta` : prenda.nombre;
      $("fijar").textContent = yaPuesta ? "Quitar esta prenda" : "Fijar esta prenda";
      $("fijar").classList.toggle("quitar", yaPuesta);
      $("fijar").disabled = !puedeGenerar;
    }

    // Fila "Puesto"
    const fila = $("puesto");
    fila.querySelectorAll("button, .vacio").forEach((x) => x.remove());
    const ids = ORDEN.map((t) => puesto.get(t)).filter(Boolean);
    if (!ids.length) fila.insertAdjacentHTML("beforeend", '<span class="vacio">nada todavía</span>');
    for (const id of ids) {
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = `${prendaPorId[id].nombre} ✕`;
      b.setAttribute("aria-label", `Quitar ${prendaPorId[id].nombre}`);
      b.disabled = !puedeGenerar;
      b.addEventListener("click", () => cambiarConjunto((p) => p.delete(prendaPorId[id].tipo)));
      fila.appendChild(b);
    }

    // Girar y vistas: solo cuando hay algo puesto
    $("girar").hidden = $("vistas").hidden = ids.length === 0;
    $("girar").disabled = !puedeGenerar;
    $("vistas").querySelectorAll("button").forEach((b) => {
      b.setAttribute("aria-pressed", b.dataset.vista === vista);
      b.disabled = !puedeGenerar;
    });

    $("usar-foto").disabled = !puedeGenerar;
    $("usar-modelo").hidden = !miFoto;
    $("usar-modelo").disabled = ocupado;
    $("velo").hidden = !ocupado;

    // El mensaje de WhatsApp nombra solo prendas reales de la tienda, nunca las de ejemplo.
    const nombres = ids.map((id) => prendaPorId[id]).filter((p) => !p.ejemplo).map((p) => p.nombre);
    const texto = nombres.length
      ? `Hola ${datos.marca}, me probé en el probador: ${nombres.join(", ")}. ¿Me pasan precio y talles?`
      : `Hola ${datos.marca}, estuve mirando el probador. ¿Me cuentan qué tienen disponible?`;
    $("la-quiero").href = `${datos.whatsapp}?text=${encodeURIComponent(texto)}`;
    $("la-quiero").textContent = nombres.length ? "Lo quiero: consultar por WhatsApp" : "Consultar por WhatsApp";
  }

  function ver(url, generada) {
    persona.src = url;
    $("leyenda").textContent = generada ? LEYENDAS[vista] : "";
    $("leyenda").hidden = !generada;
  }

  function avisar(texto) {
    $("mensaje").textContent = texto || "";
    $("mensaje").hidden = !texto;
  }

  // ---------- Pedir la foto ----------

  async function probar(anterior) {
    const pedido = clave();
    avisar("");
    if (!pedido) {
      vista = "frente";
      ver(base(), false);
      return refrescar();
    }
    const guardada = `${pedido}|${vista}`;
    if (hechas.has(guardada)) {
      ver(hechas.get(guardada), true);
      return refrescar();
    }

    ocupado = true;
    refrescar();
    const cuerpo = new FormData();
    cuerpo.append("prendas", pedido);
    cuerpo.append("vista", vista);
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
      hechas.set(guardada, url);
      ver(url, true);
    } catch (e) {
      // Si falló, todo vuelve a como estaba antes del pedido.
      puesto = anterior.puesto;
      vista = anterior.vista;
      avisar(e.message);
    } finally {
      ocupado = false;
      refrescar();
    }
  }

  function cambiarConjunto(cambio) {
    if (ocupado || !datos.activo) return;
    const anterior = { puesto: new Map(puesto), vista };
    cambio(puesto);
    vista = "frente"; // un conjunto nuevo siempre se ve primero de frente
    probar(anterior);
  }

  function cambiarVista(nueva) {
    if (ocupado || !datos.activo || nueva === vista || !clave()) return;
    const anterior = { puesto: new Map(puesto), vista };
    vista = nueva;
    probar(anterior);
  }

  $("fijar")?.addEventListener("click", () => {
    const prenda = delCentro();
    if (!prenda) return;
    cambiarConjunto((p) => {
      if (p.get(prenda.tipo) === prenda.id) return p.delete(prenda.tipo);
      // Una prenda por categoría; una prenda entera reemplaza a la de arriba y a la de abajo.
      if (prenda.tipo === "entera") ["arriba", "abajo"].forEach((t) => p.delete(t));
      if (prenda.tipo === "arriba" || prenda.tipo === "abajo") p.delete("entera");
      p.set(prenda.tipo, prenda.id);
    });
  });

  $("girar").addEventListener("click", () => {
    const vistas = ["frente", "perfil", "espalda"];
    cambiarVista(vistas[(vistas.indexOf(vista) + 1) % 3]);
  });
  $("vistas").addEventListener("click", (e) => {
    const boton = e.target.closest("button");
    if (boton) cambiarVista(boton.dataset.vista);
  });

  // ---------- La foto de la clienta ----------

  function cambiarPersona(foto) {
    for (const url of hechas.values()) URL.revokeObjectURL(url);
    hechas.clear();
    puesto = new Map();
    vista = "frente";
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
  $("usar-modelo").addEventListener("click", () => !ocupado && cambiarPersona(null));

  if (categoria) armarRueda();
  refrescar();
})();
