# Estilo de los reels de @mi.estado51

Sacado de un reel publicado («Te prometen un 20 % con un alquiler normal», 41 s, 720×1280, con voz).

## Estructura
1. **Gancho (0–5 s):** retrato de Tony recortado en arco (fondo claro, borde fino) sobre un b-roll desenfocado (monedas). Debajo, el gancho completo en 4 líneas.
2. **Cuerpo, en 6 bloques:** cada bloque tiene su propio b-roll (edificio, pared, ciudad al atardecer, manos con bolígrafo, teclado, oficina). Arriba a la derecha va el contador `01 / 06` … `06 / 06`.
3. **Cierre (~33–38 s):** fondo tinta con textura, Tony en círculo arriba, la llamada a la acción en 5 líneas y el logotipo «ESTADO 51» abajo. Ejemplo: «Guarda este reel y síguenos si prefieres los números a las promesas».
4. **Final (~38–41 s):** se oscurece y aparece el icono de Instagram con `@MI.ESTADO51`.

## Elementos fijos
- **Arriba a la izquierda:** fase del Método (`M · MAPEA`) en IBM Plex Mono pequeña, cal, con un subrayado corto en terracota.
- **Arriba a la derecha:** placa 51 en el gancho y contador `NN / 06` en el cuerpo.
- **A la izquierda, a media altura:** icono de Instagram con `@MI.ESTADO51` debajo, pequeño.
- **Bajo los subtítulos:** avatar circular de Tony (borde terracota) y la palabra `TONY` en mono.

## Subtítulos
- Van palabra a palabra al ritmo de la voz: 2 líneas de 2–4 palabras, centradas.
- Usan Archivo Black en mayúsculas, color cal, grandes (unos 100 px a 1080 de ancho).
- La palabra que se está diciendo va sobre una caja terracota con las esquinas un poco redondeadas.
- En el cierre, la caja de la palabra activa pasa a arcilla con el texto en tinta.
- Sobre el b-roll hay una capa oscura (tinta) para que se lea el texto.

## Audio
- La voz de Tony va en off durante todo el vídeo. Los subtítulos siguen la voz.

## Decisiones (28/10/2026)
- **Tony se queda**: voz en off, retrato en arco y avatar, aunque `BRAND.md` dice «sin caras y sin personaje».
- **Tamaño de subtítulos**: se copia el de los reels publicados (unos 100 px a 1080 de ancho), no el 36–48 px de `BRAND.md` 7.3.
- **Guiones**: reescritos según `BRAND.md` (sin «invertir/inversión», sin «Comenta PALABRA»).

## Cómo se genera
`python3 herramientas/render_reel.py reels/<reel>.json` (ver la cabecera del script para el formato del JSON).
Mientras no lleguen los originales, se usan recortes provisionales de un reel publicado (`provisional/`) y fondo tinta.
