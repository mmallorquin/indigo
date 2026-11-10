"""Prueba la app web de punta a punta con el Claude falso (sin gastar API)."""

import io

import pytest
from agent_framework.anthropic import AnthropicClient
from fastapi.testclient import TestClient
from PIL import Image

from tests.test_catalogo import RAIZ, AnthropicFalso


@pytest.fixture
def cliente(monkeypatch):
    monkeypatch.setenv("APP_PASSWORD", "clave-de-prueba")
    monkeypatch.delenv("AZURE_STORAGE_ACCOUNT", raising=False)
    from agente_catalogo import cargar_marca, crear_agente
    from app import main

    falso = AnthropicClient(api_key="test", model="claude-haiku-4-5", anthropic_client=AnthropicFalso())
    monkeypatch.setattr(main, "_agente", crear_agente(cargar_marca(RAIZ / "marca.toml"), client=falso))
    return TestClient(main.app)


def foto_jpg() -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (600, 800), "skyblue").save(buffer, format="JPEG")
    return buffer.getvalue()


def test_salud_sin_contrasena(cliente):
    assert cliente.get("/salud").json()["estado"] == "ok"


def test_pide_contrasena(cliente):
    assert cliente.get("/").status_code == 401
    assert cliente.get("/", auth=("indigo", "otra")).status_code == 401


def test_sin_app_password_no_atiende(cliente, monkeypatch):
    monkeypatch.delenv("APP_PASSWORD")
    assert cliente.get("/", auth=("indigo", "")).status_code == 503


def test_subir_foto_y_ver_ficha(cliente):
    auth = ("indigo", "clave-de-prueba")
    r = cliente.post("/fichar", auth=auth, files={"foto": ("blusa.jpg", foto_jpg(), "image/jpeg")})
    assert r.status_code == 200
    assert "Blusa Lino Celeste" in r.text

    inicio = cliente.get("/", auth=auth)
    assert "Blusa Lino Celeste" in inicio.text

    id_ = inicio.text.split('href="/ficha/')[1].split('"')[0]
    assert cliente.get(f"/ficha/{id_}/json", auth=auth).json()["ficha"]["categoria"] == "blusa"
    assert cliente.get(f"/foto/{id_}", auth=auth).headers["content-type"] == "image/jpeg"
