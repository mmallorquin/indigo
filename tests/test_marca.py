"""Prueba que marca.toml esté completo y que la página /marca lo muestre."""

import re

from tests.test_app import cliente  # noqa: F401  (fixture)
from tests.test_catalogo import RAIZ

from agente_catalogo import cargar_marca

AUTH = ("indigo", "clave-de-prueba")
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
COLORES_QUE_USA_EL_CSS = {"olivo", "olivo-profundo", "marfil", "arena", "tinta", "salvia"}


def test_marca_toml_tiene_lo_que_leen_los_agentes():
    marca = cargar_marca(RAIZ / "marca.toml")
    for campo in ("nombre", "rubro", "ciudad", "publico", "tono", "notas"):
        assert marca[campo].strip(), f"marca.toml: falta {campo}"
    assert marca["estilos_principales"]
    assert marca["evitar"]


def test_marca_toml_tiene_la_identidad_visual():
    identidad = cargar_marca(RAIZ / "marca.toml")["identidad"]
    colores = {c["clave"]: c["hex"] for c in identidad["colores"]}
    assert COLORES_QUE_USA_EL_CSS <= colores.keys()
    # Los hex se escriben dentro del CSS: tienen que ser hex y nada más
    assert all(HEX.match(valor) for valor in colores.values())
    assert (RAIZ / "app" / "static" / identidad["logo"]).is_file()


def test_marca_pide_contrasena(cliente):  # noqa: F811
    assert cliente.get("/marca").status_code == 401


def test_marca_muestra_los_datos_de_marca_toml(cliente):  # noqa: F811
    marca = cargar_marca(RAIZ / "marca.toml")
    r = cliente.get("/marca", auth=AUTH)
    assert r.status_code == 200
    assert "#4F5533" in r.text
    assert marca["contacto"]["whatsapp_url"] in r.text
    assert marca["evitar"][0] in r.text
    assert "Cormorant Garamond" in r.text


def test_la_app_lleva_la_identidad_de_indigo(cliente):  # noqa: F811
    inicio = cliente.get("/", auth=AUTH)
    assert "--olivo:#4F5533" in inicio.text
    assert 'href="/marca"' in inicio.text
    assert "/static/marca/logo.jpg" in inicio.text


def test_logo_y_estilos_se_sirven_sin_contrasena(cliente):  # noqa: F811
    logo = cliente.get("/static/marca/logo.jpg")
    assert logo.headers["content-type"] == "image/jpeg"
    assert len(logo.content) > 1000
    assert cliente.get("/static/indigo.css").status_code == 200


def test_las_tipografias_que_nombra_el_css_existen():
    estaticos = RAIZ / "app" / "static"
    archivos = re.findall(r'url\("([^"]+)"\)', (estaticos / "indigo.css").read_text())
    assert len(archivos) == 4
    for archivo in archivos:
        assert (estaticos / archivo).is_file(), f"indigo.css nombra {archivo} y no existe"
