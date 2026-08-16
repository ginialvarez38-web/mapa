# Atlas Orbital

Un mapa del mundo en 3D: un globo terráqueo que se dibuja con WebGL a partir de
las fronteras reales de **241 países y 4.314 provincias, estados y
departamentos**, sin librerías externas y en **un solo archivo HTML** que
funciona abriéndolo con doble clic.

```
index.html      → abre esto en el navegador
```

## Qué hace

- **Globo esférico** con cada división rellena en un matiz del color de su
  país, sus fronteras y el océano sombreado. Gira arrastrando el ratón (o el
  dedo), con inercia.
- **Dos niveles**: el botón `Divisiones` alterna entre el mapa por provincias y
  el mapa por países. El nivel activo manda también al señalar: al pinchar se
  selecciona la división o el país, según lo que esté a la vista.
- **Ficha de cada región**: tipo (provincia, estado, óblast, prefectura…), país
  al que pertenece —pinchable, para saltar al país entero—, superficie, punto
  central, antípoda y hora solar del lugar.
- **Índice lateral** con los 241 países y su superficie. El buscador acepta
  también divisiones: escribe «navarra», «baviera» o «chubut».
- **Modo día/noche**: ilumina el globo con la posición real del Sol calculada
  para el instante actual, con su terminador y el halo atmosférico encendido
  solo en el limbo iluminado.
- **Dos estilos**: `Noche` (globo sobre fondo estrellado) y `Carta` (aspecto de
  atlas político impreso). Por defecto sigue el tema claro u oscuro del visor.
- **Retícula** de meridianos y paralelos cada 15°.
- Teclado: flechas para girar, `+` / `−` para acercar, `Inicio` para reiniciar
  la vista y `Esc` para cerrar la ficha.

## Cómo se construye

```bash
# 1. datos de origen (40 MB, no van en el repositorio)
git clone --depth 1 --filter=blob:none --sparse \
    https://github.com/nvkelso/natural-earth-vector.git /tmp/ne
git -C /tmp/ne sparse-checkout set geojson
cp /tmp/ne/geojson/ne_10m_admin_1_states_provinces.geojson data/admin1.geojson

# 2. geometría lista para la GPU  (~45 s)
python3 tools/build_mundo.py     # data/admin1.geojson → data/mundo.json

# 3. archivo único
python3 tools/bundle.py          # plantilla + datos   → index.html
```

| Archivo | Función |
| --- | --- |
| `src/globo.template.html` | La aplicación: estilos, interfaz y el motor WebGL. |
| `tools/build_mundo.py` | Divisiones, países y fronteras a partir del GeoJSON. |
| `tools/topologia.py` | Simplificación que respeta las fronteras compartidas. |
| `tools/geometria.py` | De polígonos lon/lat a triángulos sobre la esfera. |
| `tools/nombres_es.py` | Nombres de países en español. |
| `tools/bundle.py` | Inyecta los datos en la plantilla. |

## Decisiones técnicas

Dibujar 4.314 polígonos administrativos sobre una esfera, en un archivo que
tiene que caber en un navegador, plantea seis problemas. Uno por paso:

**1. Reducir 1,3 millones de puntos.** El nivel administrativo 1 de Natural
Earth trae ese detalle; el archivo final admite una fracción. Simplificar cada
división por su cuenta abre grietas: dos provincias vecinas recortan su
frontera común de forma distinta y entre ellas queda una rendija. La solución
es la de TopoJSON: cuantizar a una rejilla, cortar todos los anillos en arcos,
quedarse con **una sola copia de cada arco compartido**, simplificarlo una vez
(Douglas-Peucker) y reconstruir los anillos. Las dos vecinas usan entonces
exactamente la misma línea. Quedan 252.000 puntos, un 81% menos, sin una sola
grieta.

**2. No aplastar las islas.** Con una tolerancia fija, una isla de 20 km se
convierte en un cuadrilátero mientras una costa de 3.000 km apenas cambia. La
tolerancia se calcula sobre el tamaño del propio arco, así que cada uno se
recorta en la misma proporción — y como depende solo del arco, los dos
polígonos que lo comparten siguen calculando el mismo valor.

**3. Una sola escala.** La primera versión mezclaba países a 1:110 M con
divisiones a 1:10 M: las provincias asomaban sobre el mar y los contornos no
encajaban. Ahora toda la geometría sale del mismo origen y **las fronteras de
país se deducen de los arcos**: un arco que separa divisiones de dos países
distintos, o que no tiene división al otro lado —es decir, costa—, es frontera
de país. Se dibujan más marcadas, sobre las divisiones. Los dos países que
Natural Earth no subdivide (Bermudas y Guayana Francesa) entran como una
división única.

**4. Triangular sin cuñas.** Cada anillo se triangula por recorte de orejas,
con puente para los huecos —un país dentro de otro, como Lesoto dentro de
Sudáfrica—. El recorte trabaja sobre el trazado sin puntos colineales: una
oreja de área cero no se puede recortar y bloquea el algoritmo. Donde el
anillo se toca a sí mismo, el recorte deja algún triángulo por fuera; los que
caen fuera del polígono se descartan, y esa comprobación va **después** de
subdividir, porque un triángulo grande con el centro dentro puede dar trozos
que se salen.

**5. Curvar la geometría.** Un triángulo plano que abarca decenas de grados se
hunde bajo la superficie de la esfera. Se subdividen hasta que ninguna arista
supera los 4° de arco, con el criterio aplicado **a la arista y no al
triángulo**: así los dos triángulos que comparten una arista toman la misma
decisión y la malla queda conforme. Con el criterio por triángulo aparecían
vértices en T que se ven como rendijas, sobre todo cerca de los polos. Las
capas van a radios separados más que la flecha de esos triángulos; si no, el
relleno de la división y el del país se disputan el mismo píxel y salen
franjas de moaré.

**6. El antimeridiano.** La Antártida se almacena como una banda que salta de
+180° a −180°. Cerrada tal cual, su última arista cruza el mapa entero y corta
el resto del contorno. Se cierra bajando por el meridiano hasta el polo y
volviendo por el otro lado: el polígono vuelve a ser simple y además cubre el
polo. Ese tramo se marca como no dibujable para que no aparezca una línea
artificial sobre el hielo.

En el navegador, toda la geometría vive en un juego de búferes —uno para los
rellenos, otro para los contornos, otro para las fronteras de país— y el color
de cada división se lee de una textura-paleta indexada por atributos de
pertenencia (división y país), de modo que resaltar una provincia o un país
entero es cambiar un uniforme, no reconstruir nada. La selección no usa lectura
de píxeles: se lanza un rayo desde el cursor, se corta con la esfera, se
deshace la rotación y se resuelve el punto en polígono, con una rejilla de 6°
que reduce las 4.314 divisiones a las pocas candidatas de esa celda.

Los datos van cuantizados a enteros de 16 bits e indexados a 16 bits siempre
que caben, y codificados en base64: 4.314 divisiones, 280.000 vértices y
295.000 triángulos ocupan 5,2 MB.

## Comprobaciones

- Las fronteras compartidas coinciden vértice a vértice: ninguna grieta entre
  divisiones vecinas.
- El relleno no se sale del polígono en ninguna división salvo restos por
  debajo del 4% en 68 municipios diminutos (comunas eslovenas, distritos de
  Londres), invisibles a cualquier escala.
- Pinchando en el centro de la pantalla sobre el punto representativo de cada
  división, **4.307 de 4.314** devuelven la división correcta; las 7 restantes
  son franjas de menos de un kilómetro de ancho.
- Superficies contrastadas con las reales: España 506.716 km² (505.990),
  Italia 301.173 (301.340), Reino Unido 242.553 (242.495), Brasil 8.519.258
  (8.515.767), Japón 375.652 (377.975). Francia suma 636.524 km² porque
  Natural Earth incluye sus departamentos de ultramar.

## Datos

- Divisiones: [Natural Earth](https://www.naturalearthdata.com/), capa
  `ne_10m_admin_1_states_provinces`, dominio público. Los nombres en español
  vienen del propio conjunto de datos (`name_es`).
- Países sin divisiones y nombres de país:
  [`johan/world.geo.json`](https://github.com/johan/world.geo.json), derivado
  de Natural Earth 1:110 M, dominio público (`data/LICENSE-countries-geo-json`).

El nivel administrativo 1 no tiene la misma granularidad en todo el mundo: son
las 51 provincias de España, los 50 estados de Estados Unidos, los 27 estados
de Brasil… pero también las 110 provincias de Italia o los 224 distritos del
Reino Unido, que es como Natural Earth los publica. Las superficies son
aproximadas (±2%) por la simplificación, y las fronteras son las del conjunto
de datos de origen.
