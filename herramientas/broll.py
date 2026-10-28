"""Busca y descarga b-roll de Mixkit (licencia gratuita, uso comercial, sin atribución).

    python3 herramientas/broll.py buscar "suburban houses"
    python3 herramientas/broll.py bajar 47007

Los vídeos se guardan en broll/mixkit-<id>.mp4 (carpeta ignorada por git: se vuelve a
descargar sola cuando el render la necesita). En el JSON del reel se escribe "fondo": "mixkit:47007".
"""

import re
import subprocess
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CARPETA = RAIZ / "broll"


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def buscar(consulta):
    slug = re.sub(r"[^a-z0-9]+", "-", consulta.lower()).strip("-")
    html = _get(f"https://mixkit.co/free-stock-video/{slug}/").decode("utf-8", "replace")
    vistos = []
    for titulo, ident in re.findall(r'href="/free-stock-video/([a-z0-9-]+)-(\d+)/"', html):
        if ident not in [v[0] for v in vistos]:
            vistos.append((ident, titulo.replace("-", " ")))
    return vistos


def ruta(ident):
    return CARPETA / f"mixkit-{ident}.mp4"


def bajar(ident):
    destino = ruta(ident)
    if destino.exists():
        return destino
    CARPETA.mkdir(exist_ok=True)
    for calidad in ("1080", "720"):
        try:
            datos = _get(f"https://assets.mixkit.co/videos/{ident}/{ident}-{calidad}.mp4")
            break
        except Exception:
            continue
    else:
        raise RuntimeError(f"No se pudo descargar mixkit {ident}")
    destino.write_bytes(datos)
    return destino


def resolver(fondo):
    """Convierte "mixkit:<id>" en una ruta local (descargando si hace falta)."""
    if fondo and fondo.startswith("mixkit:"):
        return bajar(fondo.split(":", 1)[1])
    return RAIZ / fondo if fondo else None


def miniatura(ident, salida):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "2", "-i", str(bajar(ident)),
                    "-frames:v", "1", "-vf", "scale=320:-1", str(salida)], check=True)


if __name__ == "__main__":
    accion, arg = sys.argv[1], sys.argv[2]
    if accion == "buscar":
        for ident, titulo in buscar(arg):
            print(ident, titulo)
    elif accion == "bajar":
        print(bajar(arg))
