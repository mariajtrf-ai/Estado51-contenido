"""Voz en off PROVISIONAL con Piper (voz es_ES davefx, sin conexión), con tiempos por palabra.

No es la voz de Tony: sirve para revisar ritmo y subtítulos hasta tener el audio real.
    python3 herramientas/voz.py reels/01-tu-casa-no-te-paga.json
Escribe reels/<reel>.voz.wav y reels/<reel>.tiempos.json (formato que usa render_reel.py).
"""

import json
import re
import sys
import urllib.request
import wave
from pathlib import Path

import numpy as np
from piper import PiperVoice, SynthesisConfig

RAIZ = Path(__file__).resolve().parent.parent
MODELO = RAIZ / "broll" / "voces" / "es_ES-davefx-medium.onnx"
URL_MODELO = "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/davefx/medium/"

PAUSA_FRASE = 0.22
PAUSA_TRAMO = 0.45
INICIO = 0.3

UNIDADES = "cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciséis diecisiete dieciocho diecinueve veinte veintiuno veintidós veintitrés veinticuatro veinticinco veintiséis veintisiete veintiocho veintinueve".split()
DECENAS = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
CENTENAS = {1: "ciento", 2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos",
            6: "seiscientos", 7: "setecientos", 8: "ochocientos", 9: "novecientos"}


def numero(n):
    if n < 30:
        return UNIDADES[n]
    if n < 100:
        d, u = divmod(n, 10)
        return DECENAS[d] + ("" if u == 0 else " y " + UNIDADES[u])
    if n < 1000:
        c, r = divmod(n, 100)
        if n == 100:
            return "cien"
        return CENTENAS[c] + ("" if r == 0 else " " + numero(r))
    if n < 1_000_000:
        m, r = divmod(n, 1000)
        miles = "mil" if m == 1 else numero(m).replace("uno", "un") + " mil"
        return miles + ("" if r == 0 else " " + numero(r))
    m, r = divmod(n, 1_000_000)
    millones = "un millón" if m == 1 else numero(m) + " millones"
    return millones + ("" if r == 0 else " " + numero(r))


SIGLAS = {"EE. UU.": "Estados Unidos", "IBI": "ibi", "HOA": "ache o a", "CPA": "ce pe a", "LLC": "ele ele ce"}
MONEDAS = {"$": "dólares", "€": "euros", "%": "por ciento"}


def hablado(texto):
    """Convierte el texto de pantalla en texto para leer en voz alta."""
    for sigla, dicho in SIGLAS.items():
        texto = texto.replace(sigla, dicho)

    def cifra(m):
        entero = int(m.group(1).replace(".", ""))
        dicho = numero(entero)
        if m.group(2):
            dicho += " coma " + numero(int(m.group(2)))
        simbolo = m.group(3)
        if simbolo:
            if simbolo != "%" and dicho.endswith("uno"):
                dicho = dicho[:-3] + ("ún" if dicho.endswith("veintiuno") else "un")
            dicho += " " + MONEDAS[simbolo]
        return dicho

    texto = re.sub(r"(\d{1,3}(?:\.\d{3})*|\d+)(?:,(\d+))?(?:[\s ]?([$€%]))?", cifra, texto)
    return texto.replace(" ", " ")


def frases(tokens):
    actual = []
    for t in tokens:
        actual.append(t)
        if t[-1] in ".?!:;":
            yield actual
            actual = []
    if actual:
        yield actual


def recortar(audio, umbral=400):
    sonoro = np.where(np.abs(audio) > umbral)[0]
    if len(sonoro) == 0:
        return audio
    return audio[max(0, sonoro[0] - 400): sonoro[-1] + 800]


def cargar_voz():
    if not MODELO.exists():
        MODELO.parent.mkdir(parents=True, exist_ok=True)
        for sufijo in ("", ".json"):
            urllib.request.urlretrieve(URL_MODELO + MODELO.name + sufijo, str(MODELO) + sufijo)
    return PiperVoice.load(str(MODELO))


def generar(ruta_json):
    sys.path.insert(0, str(RAIZ / "herramientas"))
    from render_reel import palabras  # misma tokenización que los subtítulos

    ruta_json = Path(ruta_json)
    reel = json.loads(ruta_json.read_text(encoding="utf-8"))
    voz = cargar_voz()
    ajustes = SynthesisConfig(length_scale=reel.get("velocidad_voz", 0.9))
    sr = voz.config.sample_rate

    tramos = [reel["gancho"]] + reel["bloques"] + [reel["cierre"]]
    piezas = [np.zeros(int(INICIO * sr), dtype=np.int16)]
    t = INICIO
    tiempos = []
    for tramo in tramos:
        for frase in frases(palabras(tramo["texto"])):
            dicho = hablado(" ".join(frase))
            audio = np.concatenate([c.audio_int16_array for c in voz.synthesize(dicho, ajustes)])
            audio = recortar(audio)
            dur = len(audio) / sr
            # Reparte la duración de la frase según lo largo que es cada palabra al decirla.
            pesos = [len(hablado(p)) + 2 for p in frase]
            total = sum(pesos)
            acumulado = t
            for p, peso in zip(frase, pesos):
                d = dur * peso / total
                tiempos.append({"palabra": p, "inicio": round(acumulado, 3), "fin": round(acumulado + d, 3)})
                acumulado += d
            piezas += [audio, np.zeros(int(PAUSA_FRASE * sr), dtype=np.int16)]
            t += dur + PAUSA_FRASE
        piezas.append(np.zeros(int((PAUSA_TRAMO - PAUSA_FRASE) * sr), dtype=np.int16))
        t += PAUSA_TRAMO - PAUSA_FRASE

    base = ruta_json.with_suffix("")
    with wave.open(str(base) + ".voz.wav", "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(np.concatenate(piezas).tobytes())
    Path(str(base) + ".tiempos.json").write_text(json.dumps(tiempos, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{base}.voz.wav  ({t:.1f} s, {len(tiempos)} palabras)")


if __name__ == "__main__":
    generar(sys.argv[1])
