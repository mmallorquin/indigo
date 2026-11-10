"""Probador con IA: público sin clave, con topes de gasto, y sin guardar fotos de clientas."""

import base64
import io
import json
from types import SimpleNamespace

import pytest
from PIL import Image

import probador as pb
from tests.test_app import cliente  # noqa: F401  (fixture)

AUTH = ("indigo", "clave-de-prueba")


def imagen(color="white", tamano=(600, 800), formato="JPEG", **extra) -> bytes:
    salida = io.BytesIO()
    Image.new("RGB", tamano, color).save(salida, format=formato, **extra)
    return salida.getvalue()


class ProbadorFalso:
    """Hace de FLUX: anota lo que le piden y devuelve una imagen cualquiera."""

    def __init__(self, error=None):
        self.pedidos, self.error = [], error

    def generar(self, persona, prendas, tipos):
        self.pedidos.append(SimpleNamespace(persona=persona, prendas=prendas, tipos=tipos))
        if self.error:
            raise self.error
        return imagen("pink"), {"cost": 4.5}


@pytest.fixture
def app_limpia(cliente, monkeypatch):  # noqa: F811
    """Almacén vacío, probador falso, y dos prendas cargadas + modelo de ejemplo."""
    from almacen import AlmacenMemoria
    from app import main

    falso = ProbadorFalso()
    monkeypatch.setattr(main, "almacen", AlmacenMemoria())
    monkeypatch.setattr(main, "probador_ia", falso)
    monkeypatch.delenv("PROBADOR_TOPE_DIA", raising=False)
    monkeypatch.delenv("PROBADOR_TOPE_IP", raising=False)
    for nombre, tipo in (("Blusa lino", "arriba"), ("Jean recto", "abajo"), ("Vestido largo", "entera")):
        r = cliente.post("/probador/prendas", auth=AUTH, data={"nombre": nombre, "tipo": tipo},
                         files={"foto": ("p.jpg", imagen("navy"), "image/jpeg")}, follow_redirects=False)
        assert r.status_code == 303
    assert cliente.post("/probador/modelo", auth=AUTH, files={"foto": ("m.jpg", imagen("beige", (900, 1200)), "image/jpeg")},
                        follow_redirects=False).status_code == 303
    ids = {p["tipo"]: p["id"] for p in pb.prendas(main.almacen)}
    return SimpleNamespace(cliente=cliente, main=main, falso=falso, ids=ids)


def probar(a, prendas, foto=None, acepto="si", ip=None):
    archivos = {"foto": ("yo.jpg", foto, "image/jpeg")} if foto else None
    datos = {"prendas": prendas, **({"acepto": acepto} if foto else {})}
    return a.cliente.post("/probador/probar", data=datos, files=archivos,
                          headers={"x-forwarded-for": ip} if ip else {})


# --- Qué es público y qué no ---

def test_el_probador_es_publico_y_no_enlaza_a_lo_privado(app_limpia):
    r = app_limpia.cliente.get("/probador")
    assert r.status_code == 200
    assert "Blusa lino" in r.text and "/probador/modelo.jpg" in r.text
    assert 'href="/marca"' not in r.text and 'href="/probador/prendas"' not in r.text
    id_ = app_limpia.ids["arriba"]
    assert app_limpia.cliente.get(f"/probador/prenda/{id_}.jpg").headers["content-type"] == "image/jpeg"
    assert app_limpia.cliente.get("/probador/modelo.jpg").status_code == 200
    assert app_limpia.cliente.get("/static/probador.js").status_code == 200


def test_administrar_el_probador_pide_clave(cliente):  # noqa: F811
    foto = {"foto": ("a.jpg", imagen(), "image/jpeg")}
    assert cliente.get("/probador/prendas").status_code == 401
    assert cliente.post("/probador/prendas", data={"nombre": "x", "tipo": "abajo"}, files=foto).status_code == 401
    assert cliente.post("/probador/prendas/abc/borrar").status_code == 401
    assert cliente.post("/probador/modelo", files=foto).status_code == 401
    assert cliente.get("/", auth=AUTH).text.count('href="/probador/prendas"') == 1


# --- Generar ---

def test_con_la_modelo_genera_una_vez_y_despues_reutiliza(app_limpia):
    a = app_limpia
    r = probar(a, a.ids["arriba"])
    assert r.status_code == 200 and r.headers["content-type"] == "image/jpeg"
    assert probar(a, a.ids["arriba"]).content == r.content  # segunda vez: guardada, no se paga de nuevo
    assert len(a.falso.pedidos) == 1

    pedido = a.falso.pedidos[0]
    assert pedido.tipos == ["arriba"] and len(pedido.prendas) == 1
    with Image.open(io.BytesIO(pedido.persona)) as persona:  # medidas múltiplo de 16, como pide el modelo
        assert persona.width % 16 == 0 and persona.height % 16 == 0 and max(persona.size) <= 1024
    uso = pb.Topes(a.main.almacen).leer(a.main._hoy())
    assert uso["total"] == 1 and uso["costo"] == 4.5


def test_combina_arriba_y_abajo_en_orden(app_limpia):
    a = app_limpia
    assert probar(a, f"{a.ids['abajo']},{a.ids['arriba']}").status_code == 200
    assert a.falso.pedidos[0].tipos == ["arriba", "abajo"]


@pytest.mark.parametrize("prendas", ["", "noexiste", "ARRIBA,ENTERA", "ARRIBA,ARRIBA2"])
def test_rechaza_combinaciones_que_no_tienen_sentido(app_limpia, prendas):
    a = app_limpia
    prendas = prendas.replace("ARRIBA2", "otra").replace("ARRIBA", a.ids["arriba"]).replace("ENTERA", a.ids["entera"])
    r = probar(a, prendas or ",")
    assert r.status_code == 400 and r.json()["tipo"] == "pedido"
    assert a.falso.pedidos == []


# --- La foto de la clienta ---

def test_la_foto_de_la_clienta_exige_aceptar_y_no_se_guarda(app_limpia):
    a = app_limpia
    foto = imagen("salmon", (1500, 2000))
    assert probar(a, a.ids["abajo"], foto=foto, acepto="").status_code == 400
    assert a.falso.pedidos == []

    antes = set(a.main.almacen.listar(""))
    r = probar(a, a.ids["abajo"], foto=foto)
    assert r.status_code == 200 and r.headers["cache-control"] == "no-store"
    nuevos = set(a.main.almacen.listar("")) - antes
    assert nuevos == {f"probador/uso/{a.main._hoy()}.json"}  # solo el contador: ni la foto ni el resultado
    assert a.main.almacen.recientes(10) == []

    assert probar(a, a.ids["abajo"], foto=foto).status_code == 200  # tampoco se reutiliza: se genera de nuevo
    assert len(a.falso.pedidos) == 2


def test_a_la_ia_no_le_llegan_los_metadatos_de_la_foto():
    exif = Image.Exif()
    exif[0x010F] = "TelefonoDeLaClienta"  # fabricante; un teléfono real también guarda GPS acá
    preparada = pb.preparar_imagen(imagen("gray", (2000, 3000), exif=exif), pb.LADO_PERSONA, 16)
    with Image.open(io.BytesIO(preparada)) as img:
        assert len(img.getexif()) == 0
        assert img.size == (672, 1024)
    assert b"TelefonoDeLaClienta" not in preparada


def test_una_foto_que_no_es_foto_no_gasta(app_limpia):
    a = app_limpia
    r = probar(a, a.ids["arriba"], foto=b"esto no es una imagen")
    assert r.status_code == 400 and "no es una imagen" in r.json()["error"]
    assert a.falso.pedidos == []


# --- Topes y pausa ---

def test_tope_por_persona_y_tope_del_dia(app_limpia, monkeypatch):
    a = app_limpia
    monkeypatch.setenv("PROBADOR_TOPE_IP", "2")
    monkeypatch.setenv("PROBADOR_TOPE_DIA", "3")
    foto = imagen("salmon")
    # La IP que cuenta es la última de la lista (la que agrega Azure); la primera la puede inventar cualquiera.
    assert probar(a, a.ids["arriba"], foto=foto, ip="9.9.9.9, 1.1.1.1").status_code == 200
    assert probar(a, a.ids["arriba"], foto=foto, ip="8.8.8.8, 1.1.1.1").status_code == 200
    tercera = probar(a, a.ids["arriba"], foto=foto, ip="7.7.7.7, 1.1.1.1")
    assert tercera.status_code == 429 and tercera.json()["tipo"] == "limite"

    assert probar(a, a.ids["arriba"], foto=foto, ip="2.2.2.2").status_code == 200  # otra persona sí puede
    lleno = probar(a, a.ids["arriba"], foto=foto, ip="3.3.3.3")
    assert lleno.status_code == 429 and "límite por hoy" in lleno.json()["error"]
    assert len(a.falso.pedidos) == 3  # nunca se generó más que el tope del día

    uso = pb.Topes(a.main.almacen).leer(a.main._hoy())
    assert "1.1.1.1" not in json.dumps(uso)  # se guarda una huella, no la IP


def test_si_la_ia_falla_esa_prueba_no_cuenta(app_limpia):
    a = app_limpia
    a.falso.error = RuntimeError("se cayó")
    r = probar(a, a.ids["arriba"])
    assert r.status_code == 502 and r.json()["tipo"] == "falla"
    assert pb.Topes(a.main.almacen).leer(a.main._hoy())["total"] == 0

    a.falso.error = pb.ProbadorError("No pudimos usar esa imagen.", "rechazada", 422)
    assert probar(a, a.ids["arriba"]).status_code == 422
    assert a.main.almacen.listar("probador/cache/") == []  # un error no queda guardado como resultado


def test_en_pausa_no_genera_nada(app_limpia, monkeypatch):
    a = app_limpia
    monkeypatch.setattr(a.main, "probador_ia", None)
    r = probar(a, a.ids["arriba"])
    assert r.status_code == 503 and r.json()["tipo"] == "pausado"
    assert "en pausa" in a.cliente.get("/probador").text


def test_apagar_por_variable_de_entorno(monkeypatch):
    monkeypatch.delenv("FLUX_ENDPOINT", raising=False)
    assert pb.crear_probador() is None
    monkeypatch.setenv("FLUX_ENDPOINT", "https://ejemplo.cognitiveservices.azure.com")
    monkeypatch.setenv("PROBADOR_IA", "0")
    assert pb.crear_probador() is None


# --- Catálogo ---

def test_los_ejemplos_se_ocultan_cuando_la_tienda_carga_prendas(app_limpia):
    a = app_limpia
    ejemplo = {"id": "ej1", "nombre": "Chaleco de ejemplo", "tipo": "arriba", "creado": "2026-01-01", "ejemplo": True}
    pb.guardar_prenda(a.main.almacen, ejemplo, imagen())
    assert "Chaleco de ejemplo" not in a.cliente.get("/probador").text  # hay prendas reales
    assert "Chaleco de ejemplo" in a.cliente.get("/probador/prendas", auth=AUTH).text  # la tienda sí la ve

    for id_ in a.ids.values():
        assert a.cliente.post(f"/probador/prendas/{id_}/borrar", auth=AUTH, follow_redirects=False).status_code == 303
    publico = a.cliente.get("/probador").text
    assert "Chaleco de ejemplo" in publico and "prendas de ejemplo" in publico


@pytest.mark.parametrize("datos, archivo, mensaje", [
    ({"nombre": "Jean", "tipo": "abajo"}, b"no es una foto", "no es una imagen"),
    ({"nombre": "Jean", "tipo": "sombrero"}, None, "parte de arriba"),
    ({"nombre": "   ", "tipo": "abajo"}, None, "Falta el nombre"),
])
def test_rechaza_prendas_mal_cargadas(app_limpia, datos, archivo, mensaje):
    a = app_limpia
    antes = len(pb.prendas(a.main.almacen))
    r = a.cliente.post("/probador/prendas", auth=AUTH, data=datos,
                       files={"foto": ("p.jpg", archivo or imagen(), "image/jpeg")})
    assert r.status_code == 400 and mensaje in r.text
    assert len(pb.prendas(a.main.almacen)) == antes


# --- Las piezas que hablan con Azure, con Azure de mentira ---

def test_el_pedido_a_flux_tiene_la_forma_que_espera_azure(monkeypatch):
    flux = pb.ProbadorFlux("https://ai-ejemplo.cognitiveservices.azure.com/")
    flux._credencial = SimpleNamespace(get_token=lambda alcance: SimpleNamespace(token="token-de-prueba"))
    enviados = {}

    def post_falso(url, json, headers, timeout):
        enviados.update(url=url, json=json, headers=headers)
        cuerpo = {"data": [{"b64_json": base64.b64encode(b"jpeg").decode()}], "request_meta": {"cost": 4.5}}
        return SimpleNamespace(status_code=200, text="", json=lambda: cuerpo)

    monkeypatch.setattr(pb.httpx, "post", post_falso)
    resultado, meta = flux.generar(imagen(tamano=(768, 1024)), [b"blusa", b"jean"], ["arriba", "abajo"])

    assert resultado == b"jpeg" and meta["cost"] == 4.5
    assert enviados["url"] == "https://ai-ejemplo.cognitiveservices.azure.com/providers/blackforestlabs/v1/flux-2-pro?api-version=preview"
    assert enviados["headers"]["Authorization"] == "Bearer token-de-prueba"
    cuerpo = enviados["json"]
    assert (cuerpo["width"], cuerpo["height"]) == (768, 1024)
    assert base64.b64decode(cuerpo["input_image_2"]) == b"blusa" and base64.b64decode(cuerpo["input_image_3"]) == b"jean"
    assert "image 2 (a top)" in cuerpo["prompt"] and "image 3 (bottoms)" in cuerpo["prompt"]

    rechazo = SimpleNamespace(status_code=400, text='{"error":{"code":"content_safety_violation"}}')
    monkeypatch.setattr(pb.httpx, "post", lambda *a, **k: rechazo)
    with pytest.raises(pb.ProbadorError) as e:
        flux.generar(imagen(), [b"x"], ["arriba"])
    assert e.value.tipo == "rechazada"


def test_en_blob_lo_del_probador_no_se_mezcla_con_las_fichas():
    from azure.core.exceptions import ResourceNotFoundError

    from almacen import AlmacenBlob

    class ContenedorFalso:
        def __init__(self):
            self.blobs = {}

        def upload_blob(self, nombre, datos, overwrite, content_settings):
            self.blobs[nombre] = datos if isinstance(datos, bytes) else datos.encode()

        def list_blobs(self, name_starts_with=""):
            return [SimpleNamespace(name=n, last_modified=i) for i, n in enumerate(self.blobs) if n.startswith(name_starts_with)]

        def download_blob(self, nombre):
            if nombre not in self.blobs:
                raise ResourceNotFoundError(nombre)
            return SimpleNamespace(readall=lambda: self.blobs[nombre])

        def delete_blob(self, nombre):
            if nombre not in self.blobs:
                raise ResourceNotFoundError(nombre)
            del self.blobs[nombre]

    blob = AlmacenBlob("cuenta", contenedor=ContenedorFalso())
    blob.guardar({"id": "f1", "creado": "2026-11-10"}, imagen())
    pb.guardar_prenda(blob, {"id": "p1", "nombre": "Jean", "tipo": "abajo", "creado": "2026-11-10"}, imagen())
    pb.Topes(blob).reservar("2026-11-10", "1.1.1.1")

    assert blob.listar("") == ["f1.jpg", "f1.json", "probador/prendas/p1.jpg", "probador/prendas/p1.json",
                               "probador/uso/2026-11-10.json"]
    assert [r["id"] for r in blob.recientes(10)] == ["f1"]  # ni prendas ni contadores aparecen como fichas
    assert [p["id"] for p in pb.prendas(blob)] == ["p1"]
    assert pb.foto_prenda(blob, "../../f1") is None and blob.foto("probador/prendas/p1") is None
    pb.borrar_prenda(blob, "p1")
    pb.borrar_prenda(blob, "p1")  # borrar dos veces no rompe
    assert pb.prendas(blob) == [] and blob.ficha("f1")["id"] == "f1"
