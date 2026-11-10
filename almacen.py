"""Dónde se guardan fotos y fichas: Blob Storage en Azure, o memoria para probar local."""

import json
import os

from agente_catalogo import preparar_foto

CONTENEDOR = "fotos"


class AlmacenMemoria:
    """Se pierde al reiniciar. Solo para probar en tu Mac."""

    def __init__(self):
        self._fichas, self._fotos = {}, {}

    def guardar(self, registro: dict, foto: bytes) -> None:
        self._fichas[registro["id"]] = registro
        self._fotos[registro["id"]] = preparar_foto(foto)

    def recientes(self, n: int) -> list[dict]:
        return sorted(self._fichas.values(), key=lambda r: r["creado"], reverse=True)[:n]

    def ficha(self, id_: str) -> dict | None:
        return self._fichas.get(id_)

    def foto(self, id_: str) -> bytes | None:
        return self._fotos.get(id_)


class AlmacenBlob:
    """fotos/<id>.jpg y fotos/<id>.json en la cuenta de Storage. Entra con la identidad administrada."""

    def __init__(self, cuenta: str):
        from azure.identity import DefaultAzureCredential
        from azure.storage.blob import BlobServiceClient

        servicio = BlobServiceClient(f"https://{cuenta}.blob.core.windows.net", DefaultAzureCredential())
        self._c = servicio.get_container_client(CONTENEDOR)

    def guardar(self, registro: dict, foto: bytes) -> None:
        from azure.storage.blob import ContentSettings

        rid = registro["id"]
        self._c.upload_blob(f"{rid}.jpg", preparar_foto(foto), overwrite=True,
                            content_settings=ContentSettings(content_type="image/jpeg"))
        self._c.upload_blob(f"{rid}.json", json.dumps(registro, ensure_ascii=False), overwrite=True,
                            content_settings=ContentSettings(content_type="application/json"))

    def recientes(self, n: int) -> list[dict]:
        blobs = [b for b in self._c.list_blobs() if b.name.endswith(".json")]
        blobs.sort(key=lambda b: b.last_modified, reverse=True)
        return [json.loads(self._c.download_blob(b.name).readall()) for b in blobs[:n]]

    def ficha(self, id_: str) -> dict | None:
        return self._leer(f"{id_}.json", json.loads)

    def foto(self, id_: str) -> bytes | None:
        return self._leer(f"{id_}.jpg", lambda d: d)

    def _leer(self, nombre: str, convertir):
        from azure.core.exceptions import ResourceNotFoundError

        if not nombre.removesuffix(".json").removesuffix(".jpg").isalnum():
            return None  # evita nombres raros en la URL
        try:
            return convertir(self._c.download_blob(nombre).readall())
        except ResourceNotFoundError:
            return None


def crear_almacen():
    cuenta = os.environ.get("AZURE_STORAGE_ACCOUNT")
    return AlmacenBlob(cuenta) if cuenta else AlmacenMemoria()
