"""Renderiza un reel de Estado 51 (1080x1920) con el estilo de los reels publicados.

Uso:
    python3 herramientas/render_reel.py reels/01-tu-casa-no-te-paga.json

Estructura del JSON (rutas relativas a la raíz del repo):
    fase      etiqueta de arriba a la izquierda, p. ej. "M · MAPEA"
    gancho    {"texto": ..., "fondo": opcional}
    bloques   lista de 6 {"texto": ..., "fondo": opcional}; el contador va de 01 / 06 a 06 / 06
    cierre    {"texto": ...}
    audio     opcional: voz de Tony (wav/mp3/m4a). Sin audio, el vídeo lleva silencio.
    tiempos   opcional: JSON con [{"palabra", "inicio", "fin"}] en el mismo orden que el texto.
              Sin tiempos, se estiman a partir de la longitud de cada palabra.
    imagenes  opcional: {"retrato", "avatar", "placa", "logo"} para sustituir los provisionales.

"fondo" puede ser una imagen (zoom lento) o un vídeo. Sin fondo se usa la textura tinta.
Ver guiones/estilo-reels.md para el detalle del estilo.
"""

import json
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
W, H, FPS = 1080, 1920, 30
MARGEN = 90

TERRACOTA = (176, 83, 50)
TINTA = (34, 31, 29)
CAL = (250, 240, 232)
ARCILLA = (240, 214, 198)
ACERO = (176, 180, 182)

FUENTES = RAIZ / "herramientas" / "fuentes"
TITULAR = str(FUENTES / "ArchivoBlack-Regular.ttf")
MONO = str(FUENTES / "IBMPlexMono-Medium.ttf")
MONO_REG = str(FUENTES / "IBMPlexMono-Regular.ttf")

IMAGENES = {
    "retrato": "provisional/tony_retrato_arco.png",
    "avatar": "provisional/tony_avatar.png",
    "placa": "provisional/placa51.png",
    "logo": "provisional/logo_estado51.png",
}

NBSP = " "
TAM_SUBTITULO = 98
TAM_GANCHO = 80
TAM_CIERRE = 80
CENTRO_SUBTITULO = 1170
ANCHO_SUBTITULO = 800  # deja libre el icono de Instagram de la izquierda


def f(ruta, tam):
    return ImageFont.truetype(ruta, tam)


# ---------- fondos ----------

def textura_tinta(semilla=51):
    random.seed(semilla)
    ruido = Image.effect_noise((W // 2, H // 2), 22).resize((W, H), Image.BILINEAR)
    base = Image.new("RGB", (W, H), TINTA)
    claro = Image.new("RGB", (W, H), (58, 53, 49))
    return Image.composite(claro, base, ruido.point(lambda v: max(0, v - 110) * 2))


def cubrir(img, escala=1.0):
    r = max(W / img.width, H / img.height) * escala
    img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
    x, y = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((x, y, x + W, y + H))


class Fondo:
    """Devuelve el fotograma de fondo de un tramo, ya oscurecido para que se lea el texto."""

    def __init__(self, ruta, duracion, desenfoque=0):
        self.duracion = duracion
        self.video = None
        self.imagen = None
        self.velo = Image.new("RGB", (W, H), TINTA)
        if ruta is None:
            self.fijo = textura_tinta()
            return
        ruta = RAIZ / ruta
        if ruta.suffix.lower() in (".mp4", ".mov", ".m4v", ".webm"):
            self.video = subprocess.Popen(
                ["ffmpeg", "-loglevel", "error", "-stream_loop", "-1", "-i", str(ruta),
                 "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                 "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                stdout=subprocess.PIPE,
            )
        else:
            img = Image.open(ruta).convert("RGB")
            if desenfoque:
                img = img.filter(ImageFilter.GaussianBlur(desenfoque))
            self.imagen = img

    def fotograma(self, t):
        if self.video:
            img = Image.frombytes("RGB", (W, H), self.video.stdout.read(W * H * 3))
        elif self.imagen:
            img = cubrir(self.imagen, 1.0 + 0.08 * t / max(self.duracion, 0.1))
        else:
            return self.fijo.copy()
        return Image.blend(img, self.velo, 0.45)

    def cerrar(self):
        if self.video:
            self.video.kill()


# ---------- tiempos ----------

def palabras(texto):
    texto = texto.replace("EE. UU.", "EE." + NBSP + "UU.")
    for simbolo in ("$", "%", "€"):
        texto = texto.replace(" " + simbolo, NBSP + simbolo)
    return [p for p in texto.split(" ") if p]  # split() sin argumento también corta en NBSP


def estimar_tiempos(tramos):
    t, tiempos = 0.3, []
    for tramo in tramos:
        for p in tramo:
            dur = 0.17 + 0.037 * len(p)
            tiempos.append((t, t + dur))
            t += dur
            if p[-1] in ".:;?!»":
                t += 0.3
            elif p[-1] == ",":
                t += 0.15
        t += 0.3
    return tiempos


# ---------- piezas fijas ----------

def texto_espaciado(d, xy, texto, fuente, color, espacio, anchor_derecha=False):
    ancho = sum(d.textlength(c, font=fuente) + espacio for c in texto) - espacio
    x, y = xy
    if anchor_derecha:
        x -= ancho
    for c in texto:
        d.text((x, y), c, font=fuente, fill=color)
        x += d.textlength(c, font=fuente) + espacio


def etiqueta_fase(d, fase):
    texto_espaciado(d, (MARGEN, 290), fase.upper(), f(MONO, 32), CAL, 5)
    d.rectangle([MARGEN, 338, MARGEN + 62, 342], fill=TERRACOTA)


def contador(d, n):
    texto_espaciado(d, (W - MARGEN, 290), f"{n:02d} / 06", f(MONO_REG, 32), CAL, 4, anchor_derecha=True)


def icono_instagram(d, cx, cy, lado, color=CAL, grosor=5):
    m = lado / 2
    d.rounded_rectangle([cx - m, cy - m, cx + m, cy + m], radius=lado * 0.28, outline=color, width=grosor)
    r = lado * 0.22
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=grosor)
    p = lado * 0.06
    d.ellipse([cx + m * 0.55 - p, cy - m * 0.55 - p, cx + m * 0.55 + p, cy - m * 0.55 + p], fill=color)


def instagram_lateral(d):
    icono_instagram(d, 112, 1104, 58)
    d.text((84, 1150), "@MI.ESTADO51", font=f(MONO, 22), fill=CAL)


def recorte_circular(img, diametro):
    img = cubrir_cuadrado(img, diametro)
    mascara = Image.new("L", (diametro * 4, diametro * 4), 0)
    ImageDraw.Draw(mascara).ellipse([0, 0, diametro * 4, diametro * 4], fill=255)
    return img, mascara.resize((diametro, diametro), Image.LANCZOS)


def cubrir_cuadrado(img, lado):
    r = lado / min(img.size)
    img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
    x, y = (img.width - lado) // 2, (img.height - lado) // 2
    return img.crop((x, y, x + lado, y + lado))


def pegar_avatar(frame, avatar, cx, cy, diametro, anillo):
    img, mascara = recorte_circular(avatar, diametro)
    d = ImageDraw.Draw(frame)
    r = diametro // 2
    if anillo == TERRACOTA:
        d.ellipse([cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14], outline=(110, 55, 36), width=3)
    d.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], fill=anillo)
    frame.paste(img, (cx - r, cy - r), mascara)


def pegar_retrato_arco(frame, retrato):
    x0, y0, x1, y1 = 270, 408, 810, 1083
    ancho, alto = x1 - x0, y1 - y0
    mascara = Image.new("L", (ancho * 2, alto * 2), 0)
    dm = ImageDraw.Draw(mascara)
    dm.ellipse([0, 0, ancho * 2, ancho * 2], fill=255)
    dm.rounded_rectangle([0, ancho, ancho * 2, alto * 2], radius=40, fill=255)
    mascara = mascara.resize((ancho, alto), Image.LANCZOS)
    r = max(ancho / retrato.width, alto / retrato.height)
    img = retrato.resize((int(retrato.width * r) + 1, int(retrato.height * r) + 1), Image.LANCZOS)
    img = img.crop((0, 0, ancho, alto))
    frame.paste(img, (x0, y0), mascara)
    contorno = ImageChops.subtract(mascara, mascara.filter(ImageFilter.MinFilter(9)))
    frame.paste(Image.new("RGB", (ancho, alto), CAL), (x0, y0), contorno)


# ---------- subtítulos ----------

def partir_lineas(ps, fuente, ancho_max, d, max_palabras=3):
    lineas, actual = [], []
    for i, p in enumerate(ps):
        prueba = " ".join(ps[j] for j in actual + [i])
        if actual and (d.textlength(prueba, font=fuente) > ancho_max or len(actual) >= max_palabras):
            lineas.append(actual)
            actual = [i]
        else:
            actual.append(i)
    if actual:
        lineas.append(actual)
    return lineas


def paginas(ps, fuente, d):
    """Agrupa las palabras en páginas de 2 líneas, sin mezclar frases distintas en una página."""
    frases, actual = [], []
    for i, p in enumerate(ps):
        actual.append(i)
        if p[-1] in ".:;?!":
            frases.append(actual)
            actual = []
    if actual:
        frases.append(actual)
    resultado = []
    for frase in frases:
        lineas = partir_lineas([ps[i] for i in frase], fuente, ANCHO_SUBTITULO, d)
        lineas = [[frase[j] for j in linea] for linea in lineas]
        resultado += [lineas[i:i + 2] for i in range(0, len(lineas), 2)]
    return resultado


def dibujar_lineas(frame, ps, lineas, activa, fuente, y_centro, alineado="centro",
                   caja=TERRACOTA, texto_caja=CAL, interlineado=1.08):
    d = ImageDraw.Draw(frame)
    tam = fuente.size
    alto_linea = int(tam * interlineado)
    y = y_centro - alto_linea * len(lineas) / 2
    espacio = d.textlength(" ", font=fuente)
    for linea in lineas:
        textos = [ps[i].replace(NBSP, " ") for i in linea]
        total = sum(d.textlength(t, font=fuente) for t in textos) + espacio * (len(textos) - 1)
        x = MARGEN if alineado == "izquierda" else (W - total) / 2
        for i, t in zip(linea, textos):
            ancho = d.textlength(t, font=fuente)
            color = CAL
            if i == activa:
                d.rounded_rectangle([x - 14, y + tam * 0.02, x + ancho + 14, y + tam * 1.02], radius=10, fill=caja)
                color = texto_caja
            d.text((x, y), t, font=fuente, fill=color)
            x += ancho + espacio
        y += alto_linea


def activa_en(tiempos, t):
    for i, (ini, fin) in enumerate(tiempos):
        siguiente = tiempos[i + 1][0] if i + 1 < len(tiempos) else fin + 0.4
        if ini <= t < siguiente:
            return i
    return None


# ---------- render ----------

def render(ruta_json):
    ruta_json = Path(ruta_json)
    reel = json.loads(ruta_json.read_text(encoding="utf-8"))
    imagenes = {k: Image.open(RAIZ / v).convert("RGB") for k, v in {**IMAGENES, **reel.get("imagenes", {})}.items()}

    tramos = [reel["gancho"]] + reel["bloques"] + [reel["cierre"]]
    textos = [palabras(tr["texto"].upper()) for tr in tramos]
    if reel.get("tiempos"):
        datos = json.loads((RAIZ / reel["tiempos"]).read_text(encoding="utf-8"))
        tiempos = [(p["inicio"], p["fin"]) for p in datos]
    else:
        tiempos = estimar_tiempos(textos)
    assert len(tiempos) == sum(map(len, textos)), "Los tiempos no cuadran con el número de palabras"

    # Tiempos por tramo y límites de cada tramo.
    por_tramo, k = [], 0
    for ps in textos:
        por_tramo.append(tiempos[k:k + len(ps)])
        k += len(ps)
    inicios = [0.0] + [pt[0][0] - 0.1 for pt in por_tramo[1:]]
    fin_voz = tiempos[-1][1]
    fin_cierre = fin_voz + 1.6
    duracion = fin_cierre + 2.4
    finales = inicios[1:] + [fin_cierre]

    d_medida = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f_sub, f_gancho, f_cierre = f(TITULAR, TAM_SUBTITULO), f(TITULAR, TAM_GANCHO), f(TITULAR, TAM_CIERRE)

    salida = ruta_json.with_suffix(".mp4")
    audio = ["-i", str(RAIZ / reel["audio"])] if reel.get("audio") else ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", *audio,
         "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-t", f"{duracion:.2f}",
         "-movflags", "+faststart", str(salida)],
        stdin=subprocess.PIPE,
    )

    fondo_tinta = textura_tinta()
    fondos = {}
    for n in range(int(duracion * FPS)):
        t = n / FPS
        tramo = next((i for i in range(len(tramos)) if inicios[i] <= t < finales[i]), None)

        if tramo is None:  # pantalla final de Instagram
            frame = fondo_tinta.copy()
            p = min(1.0, (t - fin_cierre) / 0.5)
            frame = Image.blend(frame, Image.new("RGB", (W, H), (8, 7, 6)), 0.6 + 0.3 * p)
            d = ImageDraw.Draw(frame)
            icono_instagram(d, W // 2, 900, 150, grosor=12)
            d.text((W // 2, 1010), "@MI.ESTADO51", font=f(MONO, 40), fill=CAL, anchor="ma")
            ff.stdin.write(frame.tobytes())
            continue

        es_cierre = tramo == len(tramos) - 1
        if tramo not in fondos:
            for viejo in fondos.values():
                viejo.cerrar()
            ruta_fondo = tramos[tramo].get("fondo")
            if tramo == 0 and ruta_fondo is None:
                ruta_fondo = reel.get("fondo_gancho")
            fondos = {tramo: Fondo(None if es_cierre else ruta_fondo, finales[tramo] - inicios[tramo],
                                   desenfoque=12 if tramo == 0 else 0)}
        frame = fondos[tramo].fotograma(t - inicios[tramo])
        d = ImageDraw.Draw(frame)
        etiqueta_fase(d, reel["fase"])

        ps, pt = textos[tramo], por_tramo[tramo]
        activa = activa_en(pt, t)

        if tramo == 0:
            frame.paste(imagenes["placa"].resize((130, 103), Image.LANCZOS), (W - MARGEN - 130, 272))
            icono_instagram(d, W - MARGEN - 22, 505, 54)
            pegar_retrato_arco(frame, imagenes["retrato"])
            lineas = partir_lineas(ps, f_gancho, W - 2 * MARGEN, d_medida, max_palabras=8)
            dibujar_lineas(frame, ps, lineas, activa, f_gancho, 1150 + len(lineas) * TAM_GANCHO * 0.54,
                           alineado="izquierda")
        elif es_cierre:
            pegar_avatar(frame, imagenes["avatar"], W // 2, 510, 290, CAL)
            lineas = partir_lineas(ps, f_cierre, W - 2 * MARGEN - 60, d_medida, max_palabras=8)
            dibujar_lineas(frame, ps, lineas, activa, f_cierre, 1060, caja=ARCILLA, texto_caja=TINTA)
            instagram_lateral(d)
            logo = imagenes["logo"]
            frame.paste(logo, ((W - logo.width) // 2, 1450))
        else:
            contador(d, tramo)
            instagram_lateral(d)
            pags = paginas(ps, f_sub, d_medida)
            # Página visible: la que contiene la palabra activa (o la primera antes de empezar).
            idx = activa if activa is not None else 0
            pagina = next(pg for pg in pags if any(idx in linea for linea in pg))
            dibujar_lineas(frame, ps, pagina, activa, f_sub, CENTRO_SUBTITULO)
            pegar_avatar(frame, imagenes["avatar"], 168, 1444, 168, TERRACOTA)
            d.text((290, 1444), "TONY", font=f(MONO, 30), fill=CAL, anchor="lm")

        ff.stdin.write(frame.tobytes())

    for viejo in fondos.values():
        viejo.cerrar()
    ff.stdin.close()
    ff.wait()
    print(f"{salida}  ({duracion:.1f} s)")


if __name__ == "__main__":
    render(sys.argv[1])
