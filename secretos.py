"""Trae la API key y la clave de la app desde Azure Key Vault al arrancar.

En Azure, la app entra al Key Vault con su identidad administrada (id-indigo-app),
sin ninguna contraseña. En tu Mac no hace nada: las variables salen del .env.
"""

import logging
import os

log = logging.getLogger("indigo.secretos")

# nombre en Key Vault -> variable de entorno que usa la app
SECRETOS = {
    "anthropic-api-key": "ANTHROPIC_API_KEY",
    "app-password": "APP_PASSWORD",
}


def cargar_desde_key_vault() -> None:
    url = os.environ.get("KEY_VAULT_URL")
    if not url:
        return

    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient

    cliente = SecretClient(vault_url=url, credential=DefaultAzureCredential())
    for nombre, variable in SECRETOS.items():
        if os.environ.get(variable):
            continue  # si ya viene definida, manda la variable
        try:
            os.environ[variable] = cliente.get_secret(nombre).value
            log.warning("Secreto %s cargado desde Key Vault", nombre)
        except Exception as e:  # sin el secreto la app sigue viva, pero no atiende (falla cerrada)
            log.error("No pude leer %s de Key Vault: %s", nombre, e)
