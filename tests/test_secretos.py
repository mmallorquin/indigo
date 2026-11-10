"""Los secretos de Key Vault llegan a las variables de entorno (con un Key Vault falso)."""

from types import SimpleNamespace

import secretos


class KeyVaultFalso:
    def __init__(self, vault_url, credential):
        self.datos = {"anthropic-api-key": "sk-ant-desde-kv"}  # app-password no existe

    def get_secret(self, nombre):
        if nombre not in self.datos:
            raise KeyError(nombre)
        return SimpleNamespace(value=self.datos[nombre])


def test_carga_lo_que_hay_y_no_rompe_si_falta(monkeypatch):
    monkeypatch.setenv("KEY_VAULT_URL", "https://falso.vault.azure.net/")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("APP_PASSWORD", raising=False)
    import azure.keyvault.secrets as kv

    monkeypatch.setattr(kv, "SecretClient", KeyVaultFalso)
    secretos.cargar_desde_key_vault()

    import os
    assert os.environ["ANTHROPIC_API_KEY"] == "sk-ant-desde-kv"
    assert "APP_PASSWORD" not in os.environ  # falla cerrada: sin clave la app no atiende


def test_sin_key_vault_no_hace_nada(monkeypatch):
    monkeypatch.delenv("KEY_VAULT_URL", raising=False)
    secretos.cargar_desde_key_vault()  # no debe intentar conectarse a nada
