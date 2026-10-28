"""Renderiza un reel vertical (1080x1920) de Estado 51 a partir de una lista de escenas.

Uso:
    python3 herramientas/render_reel.py reels/01-tu-piso-no-es-inversion.json

Cada escena dura [inicio, fin) segundos y contiene elementos que entran animados.
Tipos de elemento:
    texto  -> texto grande en mayúsculas; las palabras entre *asteriscos* van en naranja
    fila   -> concepto a la izquierda y cifra a la derecha (la cifra cuenta hacia arriba)
    total  -> cifra grande en naranja dentro de una placa
    nota   -> texto pequeño (avisos, "ejemplo ilustrativo")
El vídeo sale sin voz: lleva una pista de audio en silencio para que Instagram lo acepte.
"""

import json
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
MARGEN = 90

FONDO_A = (20, 17, 15)
FONDO_B = (44, 33, 27)
BLANCO = (245, 240, 233)
GRIS = (170, 160, 150)
NARANJA = (217, 98, 43)

FUENTES = "/usr/share/fonts/opentype/inter/"


def fuente(peso, tam):
    return ImageFont.truetype(FUENTES + f"InterDisplay-{peso}.otf", tam)


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def fondo():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * k) for a, b in zip(FONDO_A, FONDO_B)))
    # Líneas verticales que sugieren fachadas y arquitectura.
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dc = ImageDraw.Draw(capa)
    for i, x in enumerate(range(60, W, 140)):
        alto = 700 + (i * 173) % 600
        dc.rectangle([x, H - alto, x + 90, H], outline=(255, 255, 255, 14), width=2)
        for v in range(H - alto + 40, H, 70):
            dc.rectangle([x + 20, v, x + 40, v + 30], fill=(255, 255, 255, 8))
            dc.rectangle([x + 52, v, x + 72, v + 30], fill=(255, 255, 255, 8))
    img.paste(capa, (0, 0), capa)
    # Viñeta.
    vin = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vin).ellipse([-300, -200, W + 300, H + 200], fill=255)
    vin = vin.filter(ImageFilter.GaussianBlur(200))
    oscuro = Image.new("RGB", (W, H), (8, 6, 5))
    return Image.composite(img, oscuro, vin)


def cabecera(img, pilar):
    d = ImageDraw.Draw(img)
    f = fuente("Bold", 34)
    d.rounded_rectangle([MARGEN, 110, MARGEN + d.textlength(pilar, font=f) + 44, 172], 31, outline=NARANJA, width=3)
    d.text((MARGEN + 22, 141), pilar, font=f, fill=BLANCO, anchor="lm")
    # Placa "51".
    x0 = W - MARGEN - 110
    d.rounded_rectangle([x0, 96, x0 + 110, 186], 18, fill=NARANJA)
    d.text((x0 + 55, 141), "51", font=fuente("Black", 58), fill=FONDO_A, anchor="mm")


def partir(palabras, f, ancho, d):
    lineas, actual = [], []
    for p in palabras:
        prueba = " ".join(w.strip("*") for w in actual + [p])
        if actual and d.textlength(prueba, font=f) > ancho:
            lineas.append(actual)
            actual = [p]
        else:
            actual.append(p)
    if actual:
        lineas.append(actual)
    return lineas


def dibujar_texto(d, el, y, alpha):
    tam = el.get("tam", 104)
    f = fuente("Black" if tam >= 80 else "Bold", tam)
    color_base = BLANCO if el.get("color") != "gris" else GRIS
    lineas = partir(el["texto"].split(), f, W - 2 * MARGEN, d)
    alto_linea = int(tam * 1.12)
    for i, linea in enumerate(lineas):
        limpio = [w.strip("*") for w in linea]
        total = d.textlength(" ".join(limpio), font=f)
        x = (W - total) / 2
        for w, original in zip(limpio, linea):
            color = NARANJA if original.startswith("*") else color_base
            d.text((x, y + i * alto_linea), w, font=f, fill=color + (alpha,))
            x += d.textlength(w + " ", font=f)
    return len(lineas) * alto_linea


def cifra(valor, p, formato):
    return formato.format(valor * p).replace(",", "X").replace(".", ",").replace("X", ".")


def dibujar_elemento(capa, el, y, t_local):
    p = ease((t_local - el.get("en", 0)) / 0.4)
    if p <= 0:
        return el.get("alto", 0)
    alpha = int(255 * p)
    dy = int((1 - p) * 40)
    d = ImageDraw.Draw(capa)
    tipo = el["tipo"]
    if tipo == "texto":
        return dibujar_texto(d, el, y + dy, alpha)
    if tipo == "nota":
        f = fuente("Medium", el.get("tam", 40))
        d.text((W / 2, y + dy), el["texto"], font=f, fill=GRIS + (alpha,), anchor="ma")
        return int(el.get("tam", 40) * 1.6)
    if tipo == "fila":
        f = fuente("Bold", 58)
        signo = el.get("signo", "")
        color = NARANJA if signo == "+" else BLANCO
        conteo = ease((t_local - el.get("en", 0)) / 1.0)
        d.text((MARGEN, y + dy), el["texto"], font=f, fill=BLANCO + (alpha,))
        valor = signo + cifra(el["valor"], conteo, el.get("formato", "{:,.0f} $"))
        d.text((W - MARGEN, y + dy), valor, font=f, fill=color + (alpha,), anchor="ra")
        d.line([(MARGEN, y + dy + 92), (W - MARGEN, y + dy + 92)], fill=(255, 255, 255, int(40 * p)), width=2)
        return 120
    if tipo == "total":
        f = fuente("Black", el.get("tam", 150))
        conteo = ease((t_local - el.get("en", 0)) / 1.0)
        texto = cifra(el["valor"], conteo, el.get("formato", "+{:,.0f} $"))
        escala = 0.85 + 0.15 * p
        ancho = d.textlength(texto, font=f) * escala + 120
        alto = el.get("tam", 150) * 1.5
        x0 = (W - ancho) / 2
        d.rounded_rectangle([x0, y, x0 + ancho, y + alto], 36, fill=NARANJA + (alpha,))
        fs = fuente("Black", int(el.get("tam", 150) * escala))
        d.text((W / 2, y + alto / 2), texto, font=fs, fill=FONDO_A + (alpha,), anchor="mm")
        return int(alto + 40)
    if tipo == "espacio":
        return el["alto"]
    raise ValueError(f"Tipo desconocido: {tipo}")


def render(ruta):
    reel = json.loads(Path(ruta).read_text(encoding="utf-8"))
    duracion = max(e["fin"] for e in reel["escenas"])
    base = fondo()
    cabecera(base, reel["pilar"])
    salida = Path(ruta).with_suffix(".mp4")
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(salida)],
        stdin=subprocess.PIPE,
    )
    for n in range(int(duracion * FPS)):
        t = n / FPS
        frame = base.copy().convert("RGBA")
        for esc in reel["escenas"]:
            if not esc["inicio"] <= t < esc["fin"]:
                continue
            t_local = t - esc["inicio"]
            capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            alturas = []
            # Primera pasada en una capa descartable para medir y centrar en vertical.
            medida = Image.new("RGBA", (W, H))
            for el in esc["elementos"]:
                alturas.append(dibujar_elemento(medida, dict(el, en=-10), 0, 0) + el.get("despues", 30))
            y = esc.get("y", (H - sum(alturas)) / 2 + 60)
            for el, alto in zip(esc["elementos"], alturas):
                dibujar_elemento(capa, el, y, t_local)
                y += alto
            # Salida suave al final de la escena.
            resto = esc["fin"] - t
            if resto < 0.25 and esc["fin"] < duracion:
                capa.putalpha(capa.getchannel("A").point(lambda a: int(a * resto / 0.25)))
            frame.alpha_composite(capa)
        # Barra de progreso fina abajo.
        d = ImageDraw.Draw(frame)
        d.rectangle([0, H - 10, int(W * t / duracion), H], fill=NARANJA)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    print(salida)


if __name__ == "__main__":
    render(sys.argv[1])
