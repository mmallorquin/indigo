"""Botón "Pedir por WhatsApp": la ruta /ir/whatsapp anota el clic sin datos de la persona y redirige."""

import logging
from urllib.parse import parse_qs, urlparse

import probador as pb
from tests.test_app import cliente  # noqa: F401  (fixture)
from tests.test_probador import app_limpia, imagen  # noqa: F401  (fixture)

IP = "203.0.113.9"


def ir(a, ruta):
    """Pide la ruta como lo haría un celular y devuelve la respuesta y el mensaje que quedaría escrito."""
    r = a.cliente.get(f"/ir/whatsapp/{ruta}", headers={"x-forwarded-for": IP}, follow_redirects=False)
    destino = urlparse(r.headers.get("location", ""))
    return r, destino, parse_qs(destino.query).get("text", [""])[0]


def test_id_existente_redirige_a_whatsapp_con_el_mensaje(app_limpia, caplog):
    caplog.set_level(logging.INFO, logger="indigo.clics")
    id_ = app_limpia.ids["abajo"]
    r, destino, mensaje = ir(app_limpia, id_)
    assert r.status_code == 302 and r.headers["cache-control"] == "no-store"
    assert f"{destino.scheme}://{destino.netloc}{destino.path}" == app_limpia.main.MARCA["contacto"]["whatsapp_url"]
    assert mensaje == "Hola Indigo, me interesa Jean recto. ¿Tienen en mi talle?"
    # El clic queda anotado con la prenda y la fecha, y nada de la persona.
    assert "clic_whatsapp fecha=20" in caplog.text and f"prendas={id_} pieza=-" in caplog.text
    assert IP not in caplog.text


def test_id_inexistente_da_404_y_no_anota(app_limpia, caplog):
    caplog.set_level(logging.INFO, logger="indigo.clics")
    assert ir(app_limpia, "noexiste")[0].status_code == 404
    assert ir(app_limpia, f"{app_limpia.ids['abajo']},noexiste")[0].status_code == 404
    assert "clic_whatsapp" not in caplog.text


def test_pieza_valida_va_en_el_mensaje_y_en_el_log(app_limpia, caplog):
    caplog.set_level(logging.INFO, logger="indigo.clics")
    r, _, mensaje = ir(app_limpia, f"{app_limpia.ids['abajo']}?pieza=IND-JEAN01-C1B")
    assert r.status_code == 302
    assert mensaje == "Hola, vengo por IND-JEAN01-C1B. Me interesa Jean recto. ¿Tienen en mi talle?"
    assert "pieza=IND-JEAN01-C1B" in caplog.text


def test_pieza_mal_formada_se_ignora_y_no_se_anota(app_limpia, caplog):
    caplog.set_level(logging.INFO, logger="indigo.clics")
    for mala in ("hola%20que%20tal", "IND-", "IND-JEAN01-C1B%0Aotra-linea", "IND-" + "A" * 60 + "-C1"):
        r, _, mensaje = ir(app_limpia, f"{app_limpia.ids['abajo']}?pieza={mala}")
        assert r.status_code == 302
        assert mensaje == "Hola Indigo, me interesa Jean recto. ¿Tienen en mi talle?"
    assert "pieza=-" in caplog.text
    assert "hola" not in caplog.text and "otra-linea" not in caplog.text and "AAAA" not in caplog.text


def test_conjunto_del_probador_nombra_todas_las_prendas(app_limpia):
    r, _, mensaje = ir(app_limpia, f"{app_limpia.ids['arriba']},{app_limpia.ids['abajo']}")
    assert r.status_code == 302
    assert mensaje == "Hola Indigo, me interesan Blusa lino, Jean recto. ¿Tienen en mi talle?"
    assert ir(app_limpia, ",".join(app_limpia.ids.values()))[0].status_code == 404  # 5 prendas: no es un conjunto


def test_una_prenda_de_ejemplo_no_se_nombra_ni_lleva_boton(app_limpia):
    for id_ in app_limpia.ids.values():  # la tienda muestra las de ejemplo solo si no hay prendas reales
        pb.borrar_prenda(app_limpia.main.almacen, id_)
    ejemplo = {"id": "ejjean", "nombre": "Jean de muestra", "tipo": "abajo", "creado": "2026-01-01T00:00:00+00:00",
               "ejemplo": True}
    pb.guardar_prenda(app_limpia.main.almacen, ejemplo, imagen())
    r, _, mensaje = ir(app_limpia, "ejjean")
    assert r.status_code == 302
    assert mensaje == "Hola Indigo, estuve mirando la tienda. ¿Me cuentan qué tienen disponible?"
    tienda = app_limpia.cliente.get("/tienda").text
    assert "Jean de muestra" in tienda and "/ir/whatsapp/" not in tienda and "Pedir por WhatsApp" not in tienda


def test_la_tienda_y_el_probador_llevan_el_boton(app_limpia):
    tienda = app_limpia.cliente.get("/tienda").text
    for id_ in app_limpia.ids.values():
        assert f'href="/ir/whatsapp/{id_}"' in tienda
    assert tienda.count("Pedir por WhatsApp") == len(app_limpia.ids)
    js = app_limpia.cliente.get("/static/probador.js").text
    assert "/ir/whatsapp/" in js and "Pedir por WhatsApp" in js
