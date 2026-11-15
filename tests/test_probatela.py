"""Botón "Probátela": la tienda abre el probador en la prenda elegida, sin generar ni gastar nada."""

import probador as pb
from tests.test_app import cliente  # noqa: F401  (fixture)
from tests.test_probador import AUTH, app_limpia, imagen  # noqa: F401  (fixture)


def test_cada_prenda_de_la_tienda_lleva_el_boton_probatela(app_limpia):
    tienda = app_limpia.cliente.get("/tienda").text
    for id_ in app_limpia.ids.values():
        assert f'<a class="boton secundario" href="/probador?prenda={id_}">Probátela</a>' in tienda
    assert tienda.count("Probátela") == len(app_limpia.ids)

    abajo = app_limpia.cliente.get("/tienda?tipo=abajo").text  # con el filtro, solo las de esa categoría
    assert abajo.count("Probátela") == 1 and f'href="/probador?prenda={app_limpia.ids["abajo"]}"' in abajo


def test_las_prendas_de_ejemplo_tambien_se_pueden_probar(app_limpia):
    for id_ in app_limpia.ids.values():  # la tienda muestra las de ejemplo solo si no hay prendas reales
        pb.borrar_prenda(app_limpia.main.almacen, id_)
    ejemplo = {"id": "ejjean", "nombre": "Jean de muestra", "tipo": "abajo", "creado": "2026-01-01T00:00:00+00:00",
               "ejemplo": True}
    pb.guardar_prenda(app_limpia.main.almacen, ejemplo, imagen())
    assert 'href="/probador?prenda=ejjean">Probátela</a>' in app_limpia.cliente.get("/tienda").text


def test_tienda_sin_prendas_no_muestra_el_boton(app_limpia):
    for id_ in app_limpia.ids.values():
        app_limpia.cliente.post(f"/probador/prendas/{id_}/borrar", auth=AUTH, follow_redirects=False)
    assert "Probátela" not in app_limpia.cliente.get("/tienda").text


def test_abrir_el_probador_con_una_prenda_no_genera_ni_gasta(app_limpia):
    a = app_limpia
    normal = a.cliente.get("/probador")
    antes = set(a.main.almacen.listar(""))
    for prenda in (a.ids["abajo"], "noexiste", "constructor", ""):
        r = a.cliente.get(f"/probador?prenda={prenda}")
        assert r.status_code == 200
        assert r.text == normal.text  # el servidor entrega la misma página: la rueda la acomoda el navegador
    assert a.falso.pedidos == []  # llegar desde la tienda no pide ninguna foto
    assert pb.Topes(a.main.almacen).leer(a.main._hoy())["total"] == 0
    assert set(a.main.almacen.listar("")) == antes  # ni contador ni resultados guardados


def test_el_probador_lee_la_prenda_de_la_direccion(app_limpia):
    js = app_limpia.cliente.get("/static/probador.js").text
    assert 'get("prenda")' in js
