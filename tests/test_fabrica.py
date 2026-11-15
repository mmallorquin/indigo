"""Fábrica de piezas: con un Claude falso y fotos generadas en el test (no gasta API)."""

import json

import pytest
from PIL import Image

from fabrica.__main__ import correr
from fabrica import texto

CSV = "sku,nombre,categoria,precio_gs,talles,stock,medidas,entrega,fotos,clips,prenda_probador,estado\n"


def falso_valido(sistema, pedido):
    d = {"gancho_puesto": "Así queda puesto", "gancho_precio": "Precio y talles a un mensaje",
         "detalle": "Costura reforzada y bolsillos a la vista", "combinar": ["Con blusa marfil", "Con chaleco olivo", "Con zapatillas"],
         "caption_instagram": "Mirá cómo queda.\nPedila por WhatsApp.", "caption_tiktok": "Así queda puesto",
         "hashtags": [f"#tag{i}" for i in range(10)], "alt": [f"imagen {i}" for i in range(8)]}
    return json.dumps(d), 1000, 500


@pytest.fixture
def entrada(tmp_path):
    e = tmp_path / "entrada"
    e.mkdir()
    for n in ("a.jpg", "b.jpg"):
        Image.new("RGB", (600, 800), "steelblue").save(e / n)
    return e


def csv(entrada, filas):
    (entrada / "catalogo.csv").write_text(CSV + "\n".join(filas) + "\n", encoding="utf-8")


def test_genera_todas_las_piezas(entrada, tmp_path):
    csv(entrada, ["JEAN1,Jean recto,jean,189000,36/38,,,,a.jpg|b.jpg,,,listo"])
    sal = tmp_path / "sal"
    assert correr(entrada, sal, [], 3, llamar=falso_valido) == 0
    d = sal / "JEAN1"
    for i in range(1, 6):
        assert Image.open(d / f"carrusel_0{i}.png").size == (1080, 1350)
    for i in range(1, 4):
        assert Image.open(d / f"story_0{i}.png").size == (1080, 1920)
    t = json.loads((d / "textos.json").read_text())
    assert len(t["hashtags"]) == 10 and len(t["ganchos"]) == 2 and len(t["alt"]) == 8
    w = json.loads((d / "whatsapp.json").read_text())
    assert "IND-JEAN1-S2" in w["S2"]["enlace"] and w["C1"]["enlace"].startswith("https://wa.me/595973434868")
    assert (d / "listo.json").exists() and "JEAN1" in (sal / "resumen.md").read_text()


def test_sin_precio_no_inventa(entrada, tmp_path):
    csv(entrada, ["JEAN2,Jean mom,jean,,,,,,a.jpg,,,listo"])
    sal = tmp_path / "sal"
    correr(entrada, sal, [], 3, llamar=falso_valido)
    t = json.loads((sal / "JEAN2/textos.json").read_text())
    assert set(t["datos_faltantes"]) == {"precio", "talles", "medidas", "entrega"}
    assert texto.PROHIBIDO.search("Gs. 189.000") and texto.PROHIBIDO.search("últimas unidades")


def test_rechaza_textos_con_precio_inventado(entrada, tmp_path):
    def con_precio(s, p):
        crudo, a, b = falso_valido(s, p)
        return crudo.replace("Costura reforzada", "Solo 150.000 Gs, últimas unidades"), a, b
    csv(entrada, ["JEAN3,Jean,jean,,,,,,a.jpg,,,listo"])
    sal = tmp_path / "sal"
    assert correr(entrada, sal, [], 3, llamar=con_precio) == 0
    assert not (sal / "JEAN3/listo.json").exists() and "falló" in (sal / "resumen.md").read_text()


def test_respeta_el_tope(entrada, tmp_path):
    llamadas = []
    csv(entrada, ["A,Jean,jean,,,,,,a.jpg,,,listo", "B,Blusa,blusa,,,,,,b.jpg,,,listo"])
    sal = tmp_path / "sal"
    correr(entrada, sal, [], 0.0001, llamar=lambda s, p: llamadas.append(1) or falso_valido(s, p))
    assert llamadas == [] and "tope" in (sal / "resumen.md").read_text()


def test_saltea_lo_que_ya_esta_listo(entrada, tmp_path):
    csv(entrada, ["JEAN1,Jean,jean,,,,,,a.jpg,,,listo"])
    sal = tmp_path / "sal"
    correr(entrada, sal, [], 3, llamar=falso_valido)
    def no_llamar(s, p):
        raise AssertionError("no debía llamar")
    assert correr(entrada, sal, [], 3, llamar=no_llamar) == 0
    assert "ya estaba lista" in (sal / "resumen.md").read_text()


def test_demo_solo_sin_listas_y_con_marca(entrada, tmp_path):
    csv(entrada, ["D,Demo,jean,,,,,,a.jpg,,,DEMO"])
    sal = tmp_path / "sal"
    correr(entrada, sal, [], 3, llamar=falso_valido)
    assert (sal / "D/listo.json").exists() and "DEMO" in (sal / "resumen.md").read_text()
    csv(entrada, ["D,Demo,jean,,,,,,a.jpg,,,DEMO", "J,Jean,jean,,,,,,a.jpg,,,listo"])
    sal2 = tmp_path / "sal2"
    correr(entrada, sal2, [], 3, llamar=falso_valido)
    assert not (sal2 / "D").exists() and (sal2 / "J").exists()
