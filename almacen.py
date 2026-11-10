"""Dónde se guardan fotos, fichas y prendas del probador: Blob Storage en Azure, o memoria para probar local."""

import json
import os

from agente_catalogo import preparar_foto

CONTENEDOR = "fotos"


class AlmacenMemoria:
    """Se pierde al reiniciar. Solo para probar en tu Mac."""

    def __init__(self):
        self._fichas, self._fotos, self._archivos = {}, {}, {}

    def guardar(self, registro: dict, foto: bytes) -> None:
        self._fichas[registro["id"]] = registro
        self._fotos[registro["id"]] = preparar_foto(foto)

    def recientes(self, n: int) -> list[dict]:
        return sorted(self._fichas.values(), key=lambda r: r["creado"], reverse=True)[:n]

    def ficha(self, id_: str) -> dict | None:
        return self._fichas.get(id_)

    def foto(self, id_: str) -> bytes | None:
        return self._fotos.get(id_)

    # --- archivos sueltos (los usa el probador): nombre -> contenido ---
    def escribir(self, nombre: str, datos: bytes, tipo: str) -> None:
        self._archivos[nombre] = datos

    def leer(self, nombre: str) -> bytes | None:
        return self._archivos.get(nombre)

    def borrar(self, nombre: str) -> None:
        self._archivos.pop(nombre, None)

    def listar(self, prefijo: str) -> list[str]:
        return sorted(n for n in self._archivos if n.startswith(prefijo))


class AlmacenBlob:
    """<id>.jpg y <id>.json (fichas) en la raíz; lo del probador, bajo probador/. Entra con la identidad administrada."""

    def __init__(self, cuenta: str, contenedor=None):
        if contenedor is None:
            from azure.identity import DefaultAzureCredential
            from azure.storage.blob import BlobServiceClient

            servicio = BlobServiceClient(f"https://{cuenta}.blob.core.windows.net", DefaultAzureCredential())
            contenedor = servicio.get_container_client(CONTENEDOR)
        self._c = contenedor

    def _subir(self, nombre: str, datos, tipo: str) -> None:
        from azure.storage.blob import ContentSettings

        self._c.upload_blob(nombre, datos, overwrite=True, content_settings=ContentSettings(content_type=tipo))

    def guardar(self, registro: dict, foto: bytes) -> None:
        self._subir(f"{registro['id']}.jpg", preparar_foto(foto), "image/jpeg")
        self._subir(f"{registro['id']}.json", json.dumps(registro, ensure_ascii=False), "application/json")

    def recientes(self, n: int) -> list[dict]:
        # Las fichas están en la raíz del contenedor; lo que tiene "/" es de otra cosa (prendas del probador)
        blobs = [b for b in self._c.list_blobs() if b.name.endswith(".json") and "/" not in b.name]
        blobs.sort(key=lambda b: b.last_modified, reverse=True)
        return [json.loads(self._c.download_blob(b.name).readall()) for b in blobs[:n]]

    def ficha(self, id_: str) -> dict | None:
        return self._leer(f"{id_}.json", json.loads)

    def foto(self, id_: str) -> bytes | None:
        return self._leer(f"{id_}.jpg", lambda d: d)

    # --- archivos sueltos (los usa el probador): nombre -> contenido ---
    def escribir(self, nombre: str, datos: bytes, tipo: str) -> None:
        self._subir(nombre, datos, tipo)

    def leer(self, nombre: str) -> bytes | None:
        from azure.core.exceptions import ResourceNotFoundError

        try:
            return self._c.download_blob(nombre).readall()
        except ResourceNotFoundError:
            return None

    def borrar(self, nombre: str) -> None:
        from azure.core.exceptions import ResourceNotFoundError

        try:
            self._c.delete_blob(nombre)
        except ResourceNotFoundError:
            pass

    def listar(self, prefijo: str) -> list[str]:
        return sorted(b.name for b in self._c.list_blobs(name_starts_with=prefijo))

    def _leer(self, nombre: str, convertir):
        from azure.core.exceptions import ResourceNotFoundError

        if not nombre.rsplit(".", 1)[0].isalnum():
            return None  # evita nombres raros en la URL
        try:
            return convertir(self._c.download_blob(nombre).readall())
        except ResourceNotFoundError:
            return None


def crear_almacen():
    cuenta = os.environ.get("AZURE_STORAGE_ACCOUNT")
    return AlmacenBlob(cuenta) if cuenta else AlmacenMemoria()
