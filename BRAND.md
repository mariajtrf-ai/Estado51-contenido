# Estado 51 · Manual de marca para Claude Code

> Este archivo es la fuente de verdad de la identidad visual y verbal de **Estado 51**.
> Léelo entero antes de generar cualquier pieza (carrusel, story, banner, landing, documento o email).
> Si una instrucción del usuario contradice este manual, avisa y pide confirmación antes de saltarte la regla.
> Versión 1.0 · octubre 2026 · Manual completo en PDF: `assets/E51_manual_de_marca_v1.pdf`

---

## 0. Cómo usar este archivo

- Cópialo en la raíz del proyecto como `BRAND.md` y referéncialo desde `CLAUDE.md` con una línea: `Sigue siempre BRAND.md para cualquier pieza de Estado 51.`
- Los recursos gráficos van en `assets/` con la misma estructura que el kit de marca (ZIP «Manual de marca Estado 51»):

```
assets/
├── E51_manual_de_marca_v1.pdf
├── Logos/
│   ├── SVG/   (vectores originales)
│   └── PNG/   (fondo transparente)
├── Texturas/  (post 1080×1350 y story 1080×1920, JPG)
├── Plantillas/ (PDF y PNG de referencia)
├── redes/     (perfiles, portada de Facebook, banner y marca de agua de YouTube)
└── Fuentes/   (TTF + licencias OFL)
```

- **No dibujes nunca el logo con texto ni con CSS.** Usa siempre los archivos de `assets/Logos/`.
- **No inventes colores, fuentes ni efectos.** Todo lo permitido está aquí.

---

## 1. La marca en 30 segundos

| | |
|---|---|
| **Qué es** | Marca para hispanohablantes de España y LATAM que viven fuera de EE. UU. y quieren comprar allí una propiedad, con orden y con números. |
| **Producto** | Curso de entrada (29 $) y Kit (49 $). Método propio: **Método MAPA**. |
| **Lema** | **Hay 50 estados. El 51 es el tuyo.** |
| **Concepto visual** | «La placa»: una placa de acero atornillada con el 51, como el número de la fachada de tu casa en EE. UU. La **plata** es la protagonista y la **terracota** es la pared donde se atornilla. |
| **Personalidad** | «El amigo que ya lo ha hecho y lo tiene todo ordenado»: sabio, cercano, ordenado y curioso. |
| **Promesa** | Tranquilidad y camino. **Nunca dinero.** |
| **Instagram** | `@mi.estado51` (cuenta sin caras y sin personaje) |
| **No es** | Big.U ni nada que se le parezca: nada de azul eléctrico, caras en videollamada ni «generar riqueza». |

---

## 2. Reglas no negociables

1. Solo los 6 colores de la paleta (sección 3). Nada de azules, verdes de banca, dorados ni degradados.
2. Titulares en **Archivo Black, en MAYÚSCULAS**. Lectura en **Archivo**. Cifras y etiquetas en **IBM Plex Mono**.
3. El logo sale siempre de los archivos de `assets/Logos/`. No se deforma, no se gira, no se recolorea fuera de la paleta y no lleva sombras ni brillos.
4. El acero es siempre **textura** (imagen), nunca un gris plano.
5. Texto en terracota solo a **28 px o más**. El texto largo va siempre en tinta (sobre claro) o en cal (sobre terracota o tinta).
6. Márgenes de 90 px en piezas de 1080 px de ancho.
7. Cada pieza lleva **al menos una cifra concreta**.
8. En textos públicos **no se usa «invertir» ni «inversión»**: se dice «comprar una propiedad» (sección 9).
9. Las cifras van con punto de miles, coma decimal y símbolo detrás con espacio fino o no separable: `128.000 $`, `7,2 %`.
10. Sin emojis en titulares. Como mucho uno en el pie de un post, y solo si aporta algo.

---

## 3. Color

### 3.1 Paleta

| Token | Nombre | HEX | RGB | CMYK (orientativo) | Uso |
|---|---|---|---|---|---|
| `--e51-terracota` | Terracota | `#B05332` | 176 83 50 | 0 53 72 31 | Color de marca: fondos de portada, alertas y cifras clave |
| `--e51-tinta` | Tinta | `#221F1D` | 34 31 29 | 0 9 15 87 | Todo el texto sobre claro; fondos de cierre |
| `--e51-piedra` | Piedra | `#E5DFD4` | 229 223 212 | 0 3 7 10 | Fondo de lectura (interiores) |
| `--e51-cal` | Cal | `#FAF0E8` | 250 240 232 | 0 4 7 2 | Texto sobre terracota; fondos web |
| `--e51-arcilla` | Arcilla | `#F0D6C6` | 240 214 198 | 0 11 17 6 | Bandas de conclusión, etiquetas y texto secundario sobre terracota |
| `--e51-acero` | Acero | `#B0B4B6` | 176 180 182 | 3 1 0 29 | Solo como textura; en plano, únicamente como texto secundario sobre tinta |

Gris auxiliar para texto secundario sobre piedra: `#4A433D`. Línea separadora sobre piedra: `#B0A89E`.

**Proporción en el feed:** piedra 40 % · terracota 30 % · tinta 15 % · acero 10 % · arcilla 5 %.
**Nunca más de dos slides terracota seguidas.**

### 3.2 Tokens CSS

```css
:root {
  --e51-terracota: #B05332;
  --e51-tinta:     #221F1D;
  --e51-piedra:    #E5DFD4;
  --e51-cal:       #FAF0E8;
  --e51-arcilla:   #F0D6C6;
  --e51-acero:     #B0B4B6;
  --e51-texto-secundario: #4A433D; /* sobre piedra */
  --e51-linea:     #B0A89E;        /* separadores sobre piedra */

  --e51-font-display: "Archivo Black", "Archivo", system-ui, sans-serif;
  --e51-font-body:    "Archivo", system-ui, -apple-system, "Segoe UI", sans-serif;
  --e51-font-mono:    "IBM Plex Mono", ui-monospace, Menlo, monospace;
}
```

### 3.3 Tokens JSON

```json
{
  "color": {
    "terracota": "#B05332", "tinta": "#221F1D", "piedra": "#E5DFD4",
    "cal": "#FAF0E8", "arcilla": "#F0D6C6", "acero": "#B0B4B6",
    "textoSecundario": "#4A433D", "linea": "#B0A89E"
  },
  "font": {
    "display": "Archivo Black", "body": "Archivo", "mono": "IBM Plex Mono"
  },
  "layout": { "post": [1080, 1350], "story": [1080, 1920], "margin": 90, "footerBaseline": 84 }
}
```

### 3.4 Contraste (WCAG)

| Texto sobre fondo | Ratio | Permitido para |
|---|---|---|
| Tinta sobre piedra | 12,4 | Cualquier texto |
| Tinta sobre cal | 14,6 | Cualquier texto |
| Tinta sobre acero | 7,8 | Cualquier texto |
| Piedra sobre tinta | 12,4 | Cualquier texto |
| Acero sobre tinta | 7,8 | Cualquier texto |
| Cal sobre terracota | 4,5 | Cualquier texto |
| Terracota sobre piedra | 3,8 | Solo 28 px o más |
| Terracota sobre arcilla | 3,7 | Solo 28 px o más |
| Arcilla sobre terracota | 3,7 | Solo 28 px o más |
| Terracota sobre tinta | 3,2 | Solo detalles grandes; nunca etiquetas pequeñas |
| Terracota sobre acero | 2,4 | **Prohibido** |
| Acero sobre piedra | 1,6 | **Prohibido** |

---

## 4. Tipografía

Las tres familias son gratuitas (SIL Open Font License), están en Google Fonts y en la biblioteca gratuita de Canva.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
```

Si el proyecto no puede cargar Google Fonts (PDF, render sin red), usa los TTF de `assets/Fuentes/` con `@font-face`.

| Rol | Fuente | Detalles |
|---|---|---|
| Titulares | Archivo Black | Siempre en MAYÚSCULAS, `letter-spacing: .01em`, interlineado 1,05–1,12 |
| Lectura | Archivo 400 / 700 | Interlineado 1,35–1,5 |
| Etiquetas y fases | IBM Plex Mono 500 | MAYÚSCULAS, `letter-spacing: .12em` |
| Cifras y paginación | IBM Plex Mono 400 / 500 | `font-variant-numeric: tabular-nums` |

> El logo está dibujado en **Archivo Expanded** (letra ancha). Es parte del dibujo del logo, no una fuente de texto: no la uses para titulares.

### 4.1 Escala para post 1080 × 1350

| Elemento | Estilo | Tamaño | Interlineado |
|---|---|---|---|
| Titular de portada | Archivo Black | 76–104 px | 1,08–1,10 |
| Titular de interior | Archivo Black | 56–64 px | 1,12 |
| Cifra protagonista | Archivo 700 | 120–140 px | 1,00 |
| Texto de lectura | Archivo 400 | 36–40 px | 1,35–1,40 |
| Banda de conclusión | Archivo 700 | 40–44 px | 1,25 |
| Etiqueta superior | Plex Mono 500, +12 % | 28 px | — |
| Paginación y datos | Plex Mono 400 | 26 px | — |

Titulares: **máximo 4 líneas y unas 8 palabras**. Si no cabe, divide la idea en dos slides.

### 4.2 Escala web (base 16 px)

| Elemento | Tamaño |
|---|---|
| H1 | `clamp(40px, 6vw, 88px)`, Archivo Black, mayúsculas |
| H2 | `clamp(28px, 3.4vw, 44px)`, Archivo Black, mayúsculas |
| H3 / etiqueta | 14–16 px, Plex Mono 500, mayúsculas, +12 % |
| Párrafo | 17–19 px, Archivo 400, interlineado 1,55 |
| Cifras destacadas | Plex Mono 500 |

---

## 5. Logo

### 5.1 Archivos

| Versión | Archivo | Cuándo |
|---|---|---|
| **Logo horizontal (principal)** | `Logos/SVG/E51_logo_horizontal_{tinta,piedra,terracota}.svg` | Web, documentos, cabeceras, pies de carrusel. Es la versión por defecto. |
| Símbolo en acero | `Logos/PNG/E51_simbolo_acero_transparente.png` | Portadas, reels, piezas protagonistas. Solo sobre terracota o tinta (o piedra, si es grande). |
| Símbolo en acero sobre pared | `Logos/PNG/E51_simbolo_acero_sobre_terracota.png` | Imágenes de cabecera ya compuestas |
| Símbolo plano | `Logos/SVG/E51_simbolo_{terracota,tinta,piedra}.svg` | Cuando no cabe textura: web, PDF, sellos |
| Logotipo | `Logos/SVG/E51_logotipo_{tinta,piedra,terracota}.svg` | Tamaños pequeños o textos corridos |
| Logotipo con lema | `Logos/SVG/E51_logotipo_lema_{tinta,piedra}.svg` | Cierres de vídeo, firmas, contraportadas |
| Mini | `Logos/SVG/E51_simbolo_mini_{terracota,tinta,piedra}.svg` | Favicon, avatar, marca de agua |
| Método MAPA | `Logos/SVG/E51_metodo_mapa_{tinta,piedra}.svg` | Submarca del método |
| Perfiles de redes | `redes/E51_perfil_*.png`, `redes/E51_portada_facebook.png`, `redes/E51_banner_youtube.png`, `redes/E51_marca_agua_youtube.png` | Ya publicados: no regenerar sin motivo |

**Qué versión de color usar según el fondo:**
- Fondo piedra, cal o arcilla → versión **tinta**
- Fondo terracota → versión **piedra**
- Fondo tinta → versión **piedra**
- Fondo acero → versión **tinta**
- Logo en terracota sobre claro: solo a más de 300 px de ancho.

### 5.2 Área de protección y tamaño mínimo

- **x = altura de la placa.** Deja libre al menos **x/2** alrededor del logo.
- Los SVG y PNG ya incluyen un pequeño margen interior. Al alinear, ten en cuenta ese margen.

| Versión | Mínimo en pantalla | Mínimo impreso |
|---|---|---|
| Logo horizontal | 150 px de ancho | 30 mm |
| Logotipo | 100 px | 20 mm |
| Símbolo en acero | 120 px | No se imprime |
| Símbolo plano | 48 px | 12 mm |
| Mini | 16 px | 5 mm |

Por debajo del mínimo, pasa a la versión siguiente de la tabla.

### 5.3 Prohibido

Estirar o deformar · colores fuera de la paleta · sombras, brillos o contornos · girar · poner sin contraste (acero sobre piedra) · separar «ESTADO» de la placa o cambiar el orden · reescribir el logo con una fuente.

### 5.4 Submarca Método MAPA

«MÉTODO» siempre en terracota (o arcilla sobre fondo oscuro) y «MAPA» en el color del texto. El método nunca compite con el logo de Estado 51.
Las cuatro fases se usan como **etiqueta superior** de las piezas:

| Etiqueta | Contenido |
|---|---|
| `M · MAPEA` | Presupuesto, capital real, mercado, ciudad y código postal |
| `A · ASEGURA` | Estructura, impuestos, seguros y financiación |
| `P · POSEE` | Buscar, analizar, ofertar y cerrar la compra |
| `A · ADMINISTRA` | Alquiler, gestión y números de cada mes |

---

## 6. Materiales y texturas

| Superficie | Archivo | Uso |
|---|---|---|
| Pared terracota | `Texturas/E51_textura_terracota_{post,story}.jpg` | Portadas, alertas, stories |
| Piedra | `Texturas/E51_textura_piedra_{post,story}.jpg` | Interiores, cifras, listas, documentos |
| Acero cepillado | `Texturas/E51_textura_acero_{post,story}.jpg` | Solo citas de marca y el símbolo. Nunca de fondo para texto largo. |
| Tinta | `Texturas/E51_textura_tinta_{post,story}.jpg` | Cierres, llamadas a la acción, pausas |

- En web, si no puedes usar la imagen, usa el color plano equivalente (salvo el acero, que siempre es imagen).
- **Nada de degradados, sombras decorativas, brillos, glassmorphism ni efectos de Canva.** La profundidad la da la materia.
- La única sombra permitida es la que ya trae el PNG de la placa de acero.

---

## 7. Formatos y retícula

### 7.1 Carrusel de Instagram · 1080 × 1350 px (4:5)

- Márgenes: **90 px** en los cuatro lados.
- Etiqueta superior: a **130 px** del borde superior, Plex Mono 28 px.
- Pie: línea base a **84 px** del borde inferior, con el **logo horizontal a 224 px de ancho** a la izquierda y la paginación `01 / 07` a la derecha (Plex Mono 26 px).
- La cuadrícula del perfil muestra la portada en 3:4: recorta unos 34 px por cada lado. Con márgenes de 90 px no se corta nada.
- Exporta en PNG, 1080 × 1350, sRGB.

**Los seis tipos de slide**

| # | Tipo | Fondo | Estructura |
|---|---|---|---|
| 1 | Portada | Terracota | Placa de acero centrada arriba (≈550 px de ancho) · etiqueta de fase en arcilla · titular en cal (76–104 px) · línea fina en cal · pie con logo en piedra |
| 2 | Cifras | Piedra | Etiqueta en terracota · cifra grande en terracota (Archivo 700, 132 px) · desglose en filas (concepto en Archivo, importe en Plex Mono alineado a la derecha, separadores `#B0A89E`) · banda de conclusión en arcilla con texto terracota 44 px Bold |
| 3 | Puntos | Piedra | Etiqueta · titular en tinta (64 px) · de 2 a 4 puntos numerados (número en Archivo Black terracota 64 px y texto en Archivo 38 px, con la primera frase en Bold) |
| 4 | Alerta | Terracota | Etiqueta tipo `ERROR N.º 3` en arcilla · titular grande en cal (104 px) · frase de apoyo en arcilla (40 px). **Máximo una por carrusel.** |
| 5 | Cita | Acero | Frase de marca centrada en tinta (76 px) · logo horizontal tinta centrado abajo |
| 6 | Cierre | Tinta | Placa de acero (≈300 px) · titular en cal centrado · frase en acero · `@mi.estado51` en arcilla (Plex Mono 34 px) |

**Secuencia tipo (7 slides):** Portada → Contexto (puntos) → Cifras → Puntos → Alerta → Conclusión (cifras o cita) → Cierre.

### 7.2 Story · 1080 × 1920 px

- Deja libres **250 px arriba y abajo** (botones y barra de Instagram).
- Márgenes laterales de 90 px. Logo horizontal a 260 px en la zona inferior segura.
- Tipos: aviso de post (terracota + placa + titular) y pregunta del día (piedra + titular + hueco para el sticker).

### 7.3 Reel

- Rótulo principal en Archivo Black, mayúsculas, centrado, 36–48 px en 1080 de ancho, dentro de la zona segura (250 px arriba y 350 px abajo libres).
- Subtítulo en Archivo Bold, tinta sobre banda de arcilla.
- Etiqueta de fase arriba a la izquierda en Plex Mono acero sobre tinta.
- Cierre con el logo horizontal en piedra.

### 7.4 Otros formatos ya resueltos

| Pieza | Tamaño | Zona segura |
|---|---|---|
| Perfil Instagram / Facebook | 1080 × 1080 | Recorte circular: placa sin «ESTADO» |
| Portada de Facebook (fondo piedra) | 1640 × 856 | Contenido dentro de 1522 × 624 centrado; esquina inferior izquierda libre para la foto de perfil |
| Banner de YouTube (fondo piedra) | 2048 × 1152 | Todo el contenido dentro de 1235 × 338 centrado |
| Perfil de YouTube | 800 × 800 PNG | Igual que el resto de perfiles |
| Marca de agua de YouTube | 150 × 150 PNG transparente | Placa de acero sin «ESTADO» |

---

## 8. Imagen y fotografía

La cuenta **no tiene caras ni personaje**. Se ven cosas: casas, calles, planos, números y objetos.

**Sí:** fachadas, números de casa, buzones, calles de EE. UU. · planos, documentos, calculadora, llaves sobre una mesa · luz natural y cálida, colores reales · ilustración de línea en tinta con la terracota como acento.

**No:** gente sonriendo con llaves o fajos de billetes · mansiones, coches de lujo, piscinas infinitas · filtros saturados, degradados y efectos · fotos de banco de imágenes con marca de agua · imágenes generadas con IA que parezcan fotos reales de propiedades concretas.

Sobre foto con mucho detalle, aplica una capa de tinta al 40 % y usa el texto y el logo en piedra.

---

## 9. Voz y tono

**Principio:** «Se puede. Esto es lo que tiene que salir bien.»

- De tú a tú. Tutea siempre, sin jerga de gurú ni de banco.
- Valida primero y luego di lo difícil.
- Nunca cierres puertas: nombra las condiciones.
- Promete tranquilidad y camino, **nunca dinero**.
- Un número concreto en cada pieza.
- Los términos del sector, en inglés y traducidos la primera vez: *closing* (cierre), *HOA* (cuota de comunidad), *cash flow* (lo que te queda cada mes).

**Así sí**
- «Con estos números, esta casa no. Te explico por qué y qué buscar en la siguiente.»
- «Tu primera propiedad en EE. UU., paso a paso, aunque vivas fuera.»

**Así no**
- «Genera rentas pasivas del 12 % sin moverte de casa.»
- «Hazte millonario con Sección 8: el Estado te paga.»

### 9.1 Palabras en textos públicos (posts, anuncios, bio, landing, emails)

| Evitar | Usar |
|---|---|
| invertir, inversión, inversor | comprar una propiedad, tu compra |
| rentabilidad garantizada | los números de esta casa |
| fácil, rápido | paso a paso |
| ingresos pasivos | alquiler, lo que queda cada mes |
| sin dinero | con el capital que tienes |
| hazte rico, libertad financiera | tranquilidad, orden, patrimonio |

Esto reduce el riesgo de rechazo en los anuncios de Meta. Aplícalo también a textos alternativos y nombres de archivo públicos.

### 9.2 Llamadas a la acción

- Pide **comentar, seguir la cuenta o guardar el post**. Ejemplos: «Guárdalo para cuando busques casa», «Sigue @mi.estado51 para la siguiente pieza del camino», «¿Desde qué país te gustaría comprar? Te leo en comentarios».
- **No uses el formato «comenta [PALABRA] y te lo envío»**: ahora mismo no hay guía ni lead magnet que entregar.
- Una sola llamada a la acción por pieza.

---

## 10. Checklist antes de entregar cualquier pieza

Claude Code: revisa esto **siempre** y, si puedes, renderiza la pieza a PNG y mírala antes de darla por terminada.

- [ ] Medidas exactas del formato (sección 7) y exportación en PNG sRGB.
- [ ] Solo colores de la paleta; el acero, como imagen.
- [ ] Titulares en Archivo Black y en mayúsculas, de 4 líneas o menos.
- [ ] Texto largo en tinta o cal; terracota solo a 28 px o más; ninguna combinación prohibida.
- [ ] Márgenes de 90 px; pie a 84 px con logo y paginación (en carruseles).
- [ ] Logo desde `assets/Logos/`, en la versión de color correcta, por encima de su tamaño mínimo y con su área de protección.
- [ ] Al menos una cifra concreta, con formato `128.000 $` / `7,2 %` y sin cortes de línea entre número y símbolo (usa `&nbsp;`).
- [ ] Ninguna palabra de la lista «Evitar».
- [ ] Ortografía, tildes y signos de apertura (¿ ¡) revisados.
- [ ] La portada lleva la etiqueta de fase del Método MAPA.
- [ ] La última slide pide guardar, seguir o comentar, sin «comenta PALABRA».
- [ ] Sin degradados, sombras añadidas, brillos ni emojis en titulares.

---

## 11. Plantilla de referencia (HTML) · portada de carrusel

Úsala como punto de partida para renderizar slides con un navegador sin interfaz (por ejemplo, Playwright con `page.screenshot`) a 1080 × 1350.

```html
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@400;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{--t:#B05332;--k:#221F1D;--p:#E5DFD4;--cal:#FAF0E8;--c:#F0D6C6;--a:#B0B4B6}
  *{margin:0;padding:0;box-sizing:border-box}
  .slide{width:1080px;height:1350px;position:relative;overflow:hidden;
         background:url(assets/Texturas/E51_textura_terracota_post.jpg) center/cover}
  .slide > *{position:absolute}
  .placa{left:265px;top:110px;width:550px}
  .fase{left:90px;top:720px;font:500 28px "IBM Plex Mono";letter-spacing:.12em;color:var(--c)}
  .titular{left:90px;top:780px;width:900px;font:76px/1.1 "Archivo Black";
           text-transform:uppercase;letter-spacing:.01em;color:var(--cal)}
  .linea{left:90px;right:90px;bottom:170px;height:2px;background:var(--cal)}
  .logo{left:90px;bottom:84px;width:224px}
  .pag{right:90px;bottom:92px;font:400 26px "IBM Plex Mono";color:var(--cal)}
</style>
</head>
<body>
  <section class="slide">
    <img class="placa" src="assets/Logos/PNG/E51_simbolo_acero_transparente.png" alt="">
    <div class="fase">M · MAPEA</div>
    <div class="titular">Antes de mirar casas, mira el código postal.</div>
    <div class="linea"></div>
    <img class="logo" src="assets/Logos/PNG/E51_logo_horizontal_piedra.png" alt="Estado 51">
    <div class="pag">01&nbsp;/&nbsp;07</div>
  </section>
</body>
</html>
```

Para el resto de tipos de slide, cambia el fondo y los colores según la tabla de la sección 7.1. El resto de la estructura (márgenes, pie, etiqueta) se mantiene.
