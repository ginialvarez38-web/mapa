# Atlas Orbital

Un mapa del mundo en 3D: un globo terráqueo que se dibuja con WebGL a partir de
las fronteras reales de **249 países y 4.322 provincias, estados y
departamentos**, con **7.358 ciudades** y **3.536 accidentes naturales** —cordilleras, desiertos,
mesetas, cumbres, ríos, lagos y glaciares—, sin librerías externas y en **un
solo archivo HTML** que funciona abriéndolo con doble clic.

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
- **Campaña**: el botón `Campaña` lanza una invasión que se libra **celda a
  celda** sobre una rejilla de cuarto de grado —342.730 cuadros de tierra de
  unos 28 km—, **sobre el mapa político de siempre**: los colores de cada país,
  el relieve y las ciudades siguen ahí, y lo ocupado se pinta translúcido
  encima, con la línea del frente marcada. No hay turnos, ni botón de ataque, ni
  panel de órdenes: **se juega tocando el mapa**. Tocas terreno ajeno y el
  frente empuja hacia allí solo; tocas terreno tuyo y ahí se pone el peso del
  ataque. Como avanza en línea y no en punta, salen **salientes** por donde el
  terreno cede, **ciudades rodeadas** que aguantan dentro de tu territorio y
  **bolsas** cortadas del grueso enemigo, que se rinden solas. Nada es
  inventado: la guarnición de cada celda sale del ejército de su división
  —población de sus ciudades y superficie— repartido entre las celdas que
  ocupa, la resistencia de la altura real del terreno, y las plazas fuertes de
  las 7.358 ciudades del mapa. Cada división a la vista lleva **la bandera de
  quien la tiene**: la del invasor donde ya manda y la del defensor donde
  todavía resiste, de modo que se lee de un vistazo quién tiene qué.
- **Capitales y ciudades**: 7.358 poblaciones con su nombre en español, de
  las que **265 son capitales** —redondel con anillo, como en cualquier atlas—
  y 2.324, capitales de provincia. Van por importancia: desde el espacio solo
  se ven las capitales y las grandes aglomeraciones, y cada acercamiento
  destapa el siguiente escalón hasta los pueblos de menos de 5.000 habitantes.
  Se pinchan para ver su población, su región —que lleva a la división del
  mapa— y su hora solar, y la ficha de cada país trae su capital.
- **Fronteras de todos los países**: 8.951 tramos, de los que 2.054 son
  límites terrestres entre dos países y el resto, costa. Se dibujan en dos
  colores —la costa perfila la tierra, el límite político va encima— y el
  botón `Fronteras` apaga solo los segundos, para dejar un mapa físico limpio.
  Al seleccionar un país se traza **su contorno entero**, islas incluidas, y su
  ficha dice **con quién limita**: España → Andorra, Francia, Gibraltar,
  Marruecos, Portugal.
- **Ficha de cada región**: tipo (provincia, estado, óblast, prefectura…), país
  al que pertenece —pinchable, para saltar al país entero—, superficie, punto
  central, antípoda y hora solar del lugar.
- **Índice lateral** con los 249 países y su superficie. El buscador acepta
  también divisiones y accidentes: escribe «navarra», «baviera», «chubut»,
  «himalaya», «aconcagua» o «sahara».
- **Relieve**: el botón `Relieve` apaga los colores políticos y pinta la
  geografía física — 225 cordilleras, 72 mesetas, 58 desiertos, llanuras,
  cuencas, humedales, 289 masas de hielo y 1.270 lagos, con **1.057 ríos con
  nombre en español** y **632 cumbres rotuladas con su altitud** (Everest
  8.848 m, Aconcagua 6.959 m…). Cada río aparece a su altura: los grandes de
  lejos, los afluentes solo cuando ya estás encima.
- **Todo se puede pinchar**: con el relieve encendido, pinchar el globo
  selecciona el accidente natural que haya bajo el cursor —gana el más
  concreto, un lago antes que la cuenca que lo contiene— y su ficha da el
  tipo, la superficie y **la cumbre más alta que contiene**: Himalaya →
  Everest, Andes → Aconcagua, Alpes → Mont Blanc. Si no hay ninguno, se
  selecciona la división de debajo; con el relieve apagado, manda siempre lo
  administrativo.
- **Relieve en 3D**: el botón `3D` levanta el terreno sobre la esfera, con
  sombreado de laderas iluminado desde el noroeste. Las fronteras, los ríos y
  las divisiones suben con él, así que una frontera trepa por la cordillera en
  vez de atravesarla.
- **Modo día/noche**: ilumina el globo con la posición real del Sol calculada
  para el instante actual, con su terminador y el halo atmosférico encendido
  solo en el limbo iluminado.
- **Dos estilos**: `Noche` (globo sobre fondo estrellado) y `Carta` (aspecto de
  atlas político impreso). Por defecto sigue el tema claro u oscuro del visor.
- **Zoom hasta 127 km de altitud**, la escala a la que se sigue el curso de un
  río o se reconoce la forma de un lago: 1.270 lagos y 2.442 tramos de río a
  1:10 M, con los afluentes apareciendo a medida que te acercas. El arrastre
  es de agarre exacto en corto —el punto se queda bajo el cursor— y se acelera
  en las vistas lejanas.
- **Retícula** de meridianos y paralelos cada 15°.
- En campaña, el índice deja de ser alfabético: delante lo que puedes atacar
  ahora, con su ejército, y el mapa se pone en blanco político —sin relieve ni
  ciudades— para que se lea la partida. Al salir vuelve como estaba.
- Teclado: flechas para girar, `+` / `−` para acercar, `Inicio` para reiniciar
  la vista y `Esc` para cerrar la ficha.

## Cómo se construye

```bash
# 1. datos de origen (40 MB, no van en el repositorio)
git clone --depth 1 --filter=blob:none --sparse \
    https://github.com/nvkelso/natural-earth-vector.git /tmp/ne
git -C /tmp/ne sparse-checkout set geojson
cp /tmp/ne/geojson/ne_10m_admin_1_states_provinces.geojson data/admin1.geojson
for c in 10m_geography_regions_polys 10m_geography_regions_elevation_points \
         10m_geography_regions_points 10m_rivers_lake_centerlines \
         10m_lakes 50m_glaciated_areas 10m_populated_places; do
  cp /tmp/ne/geojson/ne_$c.geojson data/$c.geojson
done

# 2. geometría lista para la GPU  (~50 s)
python3 tools/build_mundo.py     # divisiones y fronteras → data/mundo.json
python3 tools/build_relieve.py   # geografía física       → data/relieve.json
python3 tools/build_ciudades.py  # capitales y ciudades   → data/ciudades.json

# 3. archivo único
python3 tools/bundle.py          # plantilla + datos      → index.html
```

| Archivo | Función |
| --- | --- |
| `src/globo.template.html` | La aplicación: estilos, interfaz y el motor WebGL. |
| `tools/build_mundo.py` | Divisiones, países y fronteras a partir del GeoJSON. |
| `tools/build_relieve.py` | Cordilleras, desiertos, cumbres, ríos, lagos, hielo y la rejilla de alturas. |
| `tools/build_ciudades.py` | Capitales y ciudades, con su rango de aparición. |
| `tools/topologia.py` | Simplificación que respeta las fronteras compartidas. |
| `tools/geometria.py` | De polígonos lon/lat a triángulos sobre la esfera. |
| `tools/nombres_es.py` | Nombres de países en español. |
| `tools/nombres_rios.py` | Nombres de ríos en español y arreglos del origen. |
| `tools/banderas.py` | Las banderas, descritas con franjas y un emblema. |
| `tools/bundle.py` | Inyecta los datos en la plantilla. |

## Decisiones técnicas

Dibujar 4.322 polígonos administrativos sobre una esfera, en un archivo que
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
de país. Cada tramo se guarda con su clase —costa o límite terrestre— y con
los países que separa, así que la lista de vecinos de la ficha y las líneas
del globo salen del mismo sitio y no se pueden contradecir. Los países que
Natural Earth no subdivide entran como una división única.

**3b. Que no falte ningún país.** Las divisiones por debajo de 20 km² no se
dibujan: a esa escala son un punto y multiplican el peso del archivo. Pero
Mónaco, San Marino, Gibraltar, Anguila o Nauru están repartidos en distritos
de pocos km² y **todos** caían por debajo del umbral: el país entero
desaparecía del mapa aunque su costa se siguiera dibujando, con un tramo de
frontera huérfano al que no pertenecía ningún país. Ahora, cuando un país se
queda sin una sola división, vuelve entero y en una pieza, sin pasar por el
mínimo. Son diez, y con ellos son 249 los países del atlas. En la dirección
contraria, Natural Earth cuelga algunos territorios de su metrópoli —la
Guayana Francesa figura dentro de Francia—: comparando el código de *geounit*
se evita dibujarlos dos veces, con la costa y la frontera duplicadas encima.

**3c. Que ninguna capital falte, y que un punto se pueda pinchar.** Natural
Earth no marca capital de país en 41 territorios: Nuuk o Papeete figuran como
«capital de región», y en las Feroe, las Cook o las Marianas la sede aparece
como una capital de provincia más. Se resuelven por reglas —una capital de
región es la capital de su territorio; si a un país le queda una sola ciudad
marcada como capital, es esa— y las 16 que ni así están se añaden a mano, con
la advertencia de que van a mano. Quedan 235 países con capital de 249: los 14
restantes son la Antártida, bases militares y atolones deshabitados.

Y un detalle que cambia el uso: el **punto se dibuja siempre, el rótulo solo si
cabe**. Al principio una ciudad cuyo nombre chocaba con el de su provincia
desaparecía entera, y con ella la posibilidad de pincharla. Ahora el redondel
está siempre —es lo que dice «aquí hay una ciudad»— y el nombre entra cuando
hay hueco, como en un mapa de papel.

**3h. 249 banderas sin una sola imagen.** La política de seguridad del visor no
deja pedir nada a otro servidor, así que las banderas en PNG no eran una opción:
pesarían más que el mapa entero. Cada una se describe con unas pocas franjas y
un emblema —`tools/banderas.py`— y se dibuja en el lienzo: 158 de franjas, 38
verticales, 28 con enseña británica, 13 de aspa, 8 de cruz nórdica y 4 de cruz
centrada. Es lo que se distingue en un rectángulo de 18 × 12, que es el tamaño
al que se ven. Los escudos, las águilas y los cedros se resuelven con una marca
del color correcto en el sitio correcto: a ese tamaño un escudo es una mancha.
Son esquemáticas a propósito, no reproducciones exactas.

**3g. Que se vea sobre el mapa de siempre, y sin panel.** Las dos primeras
versiones jugables fallaban en lo mismo: para jugar había que cambiar el mapa
—apagar el relieve, las ciudades y el color de los países— y había que hablar
con un panel de botones. Ahora la ocupación se pinta **encima** del mapa
político, translúcida y con el borde marcado, leyendo la textura de celdas
dentro del sombreador de tierra; y las órdenes son toques en el mapa, sin
turnos ni botones, con una tira de estado que sólo dice cuántas celdas llevas,
cuántas tropas tienes y contra quién estás.

Que el avance parezca una invasión costó tres intentos. Empujando siempre hacia
lo más cercano al objetivo, el frente salía como **un hilo de una celda de
ancho**. Premiar las celdas con más lados propios lo ensanchó un poco, pero no
bastaba: una celda al lado del hilo tiene el mismo apoyo que la de delante.
Lo que funciona es no empujar una punta sino **una línea**: se coge el tramo de
frontera más cercano a donde has señalado y se empuja cada celda suya un paso;
donde el terreno resiste, ese punto se queda atrás y el resto sigue.

**3f. Tomar el terreno por celdas.** Conquistar provincias enteras seguía sin
parecerse a una invasión: el mapa cambiaba de color a saltos y el frente era
siempre el contorno de una provincia. La campaña se libra ahora sobre una
rejilla de 1.440 × 720 —cuarto de grado— con 342.730 celdas de tierra.

Rasterizar 4.322 polígonos a esa rejilla con el punto-en-polígono que ya usa el
mapa serían cien millones de pruebas, así que va por **barrido de líneas**, que
recorre cada arista una vez. Lo que hay que cuidar son las aristas que cruzan el
antimeridiano: en la rejilla saltan de un extremo al otro y llenarían la fila
entera de basura, de modo que se parten en el borde. Contrastada contra las
superficies reales, la rejilla da 642 mil km² para Francia (637 mil), 508 mil
para España (507 mil) y 7,72 millones para Australia (7,77).

La ocupación **no se pinta con la geometría**: va en una textura de un téxel por
celda que el sombreador de tierra lee a partir de la posición del fragmento. Por
eso el frente puede cortar una provincia por la mitad. Sólo se sube la banda de
filas que ha cambiado, porque volver a subir el megabyte entero en cada ofensiva
se notaría.

La ofensiva empuja desde toda la frontera hacia donde señalas, tomando primero
lo que queda de camino y lo que menos resiste; lo que no puede pagar lo deja
atrás. De esa sola regla salen las tres cosas: la punta avanza formando
salientes, las ciudades caras se quedan rodeadas, y el territorio que queda
separado del grueso enemigo forma bolsas. Las bolsas se sacan por componentes
conexas —la mayor es el grueso enemigo, las demás que tocan mi territorio están
embolsadas—, con un tope de tamaño: sin él, en cuanto el imperio partía Eurasia
en dos, medio continente contaba como embolsado y se rendía solo. Y una plaza
sólo está sitiada si la rodeo yo: sin esa condición, cualquier ciudad isleña
—que no tiene vecinos por tierra— salía sitiada desde el primer turno.

**3e. Conquistar por divisiones.** La primera campaña se jugaba por países, y
mirándola no se veía avanzar nada: un país entero cambiaba de color de golpe.
Pasar a las 4.322 divisiones necesitaba saber **qué división limita con cuál**,
que es otra vez el mismo arco compartido: si dos divisiones usan el mismo arco,
son vecinas. Salen 10.214 enlaces —y 270 divisiones sin ninguno—.

Esas 270 son el problema interesante. Viena está metida dentro de Baja Austria
sin compartir su anillo con nadie, así que empezar la partida en Viena dejaba
un frente vacío y la campaña muerta desde el primer turno. Los enclaves y las
islas se resuelven mirando qué división hay al otro lado del contorno, y se
hace de una vez al empezar: hacerlo cuando toque rompería la simetría —Viena
sabría de Baja Austria y Baja Austria no de Viena— y el frente dependería del
orden de conquista.

El fallo que enseñó cómo debía jugarse salió de dejar la partida corriendo
sola: el imperio tenía **143.301 hombres y atacaba con 411**. Los refuerzos
caían todos en una división de retaguardia. Ahora cada división levanta a los
suyos y se los queda, y llevarlos al frente es una decisión del jugador —que es
exactamente lo que se pedía—. Con un bot que concentra tropas antes de atacar,
la partida desde Viena termina conquistando las 4.322 divisiones en 132 turnos,
4.353 asaltos y 32 fracasos.

**3d. Un juego que no se inventa los datos.** La campaña usa lo que el mapa ya
sabía, y eso obligó a arreglar tres cosas del propio mapa. La primera: un tramo
de frontera «de costa» es el que no tiene división al otro lado, y eso incluye
las orillas de los lagos, así que Austria embarcaba tropas hacia Jersey. La
prueba buena es salir del contorno hacia el mar y ver si allí sigue habiendo
tierra —y a dos distancias, porque un hueco entre polígonos engaña a una sonda
pero no a dos—; con eso, los dieciséis países sin salida al mar que se
comprobaron tienen cero puertos y los catorce con costa los tienen. La segunda:
recortar pronto la lista de puertos dejaba a España con costa sólo en Canarias
y medía el Estrecho —14 km— como una travesía de 900; ahora se muestrea todo el
contorno y se recorta al final. La tercera: el Cosmódromo de Baikonur es un
enclave en Kazajistán cuyo anillo no comparte nadie, así que se quedaba sin
vecinos, sin costa y sin forma de conquistarlo; para los enclaves así se mira
qué país hay al otro lado de su contorno.

El equilibrio salió de jugar la partida sola. Con los ejércitos libres creciendo
un porcentaje fijo por turno, al final de la conquista el mundo fabricaba
ejércitos infinitos y ninguna partida terminaba: ahora cada país se moviliza
hasta donde da su población y ahí se para. Cinco campañas automáticas, con un
bot que decide mirando el mismo pronóstico que ve el jugador, terminan en
victoria: Estados Unidos y Japón en 38 turnos, Austria en 105, Portugal en 123 y
Mongolia —encajonada entre Rusia y China— en 172.

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

**7. Un relieve honesto sin modelo de elevación.** No hay ningún DEM a mano, y
inventarse la altura del terreno sería justo eso: inventársela. Lo que sí es
real son los polígonos de las cordilleras y las 632 cumbres con su altitud
medida. De ahí sale una rejilla de 0,5° donde cada área se levanta a **algo más
de la mitad de la altura de la cumbre más alta que contiene** —comprobada
contra el polígono, no contra su caja: con la caja, la cuenca del Amazonas
heredaba la altura de los Andes— se afila hacia los bordes con dos pasadas de
media, y las cumbres se clavan encima con su altitud exacta. El resultado es un
**relieve esquemático, exagerado 16 veces**, no un modelo del terreno; la
interfaz lo dice y el botón `3D` lo apaga. El sombreado de laderas se calcula
del gradiente de esa rejilla, una vez por vértice al cargar, así que cambiar la
exageración es mover un uniforme.

**8. Zoom hasta el río.** Acercarse a 127 km de altitud obliga a cambiar cuatro
cosas a la vez: los ríos y lagos pasan a 1:10 M —2.442 tramos ordenados por
importancia, de los que solo se dibuja el prefijo que corresponde al zoom—; el
plano de recorte cercano y el paso del teclado se hacen proporcionales a la
altura; la exageración del relieve se recoge al acercarse, porque a ×16 la
cámara acabaría dentro de la montaña; y el arrastre pasa a calcularse de la
geometría de la vista, así que en corto el punto agarrado se queda bajo el
cursor. La esfera del océano subió a 256×128 caras: a esa altura sus facetas
se notaban en el horizonte.

**9. Los ríos, uno por uno.** La capa de ríos de Natural Earth **no trae campo
`name_es`**: sus 1.367 nombres están en forma local o inglesa, y unos cuantos
llegan con los caracteres no ASCII comidos —«Rhne» por Ródano, «Gta lv» por
Göta älv, «Ro Grande de Santiago», «Pnuco», «Kiz?lirmak»—. `nombres_rios.py`
arregla las dos cosas con una tabla de 300 entradas; los ríos cuyo nombre es
igual en español (Congo, Paraná, Orinoco, Volga…) no aparecen en ella. Hay
además una corrección de trazado: Natural Earth rotula «Paraná» todo el eje
desde el Pantanal hasta el estuario, así que **el río Paraguay no existía en el
mapa**; se separa por la confluencia, junto a Corrientes.

**10. Lo físico sobre lo político.** El relieve no sustituye al mapa, se
superpone: al encenderlo, los colores políticos se apagan hacia un verde
neutro (un `mix` en el sombreador, no otra geometría) y encima se dibujan las
áreas físicas translúcidas, los lagos opacos, los ríos y las cumbres. Los
límites de una cordillera o un desierto son indicativos, así que se simplifican
mucho más que las fronteras; los lagos, que sí tienen forma reconocible,
conservan el detalle. Las cumbres son rótulos del lienzo 2D, no geometría: se
registran con su posición en pantalla al dibujarlas, y por eso se pueden
pinchar aunque midan doce píxeles.

En el navegador, toda la geometría vive en un juego de búferes —uno para los
rellenos, otro para los contornos, otro para las fronteras de país— y el color
de cada división se lee de una textura-paleta indexada por atributos de
pertenencia (división y país), de modo que resaltar una provincia o un país
entero es cambiar un uniforme, no reconstruir nada. La selección no usa lectura
de píxeles: se lanza un rayo desde el cursor, se corta con la esfera, se
deshace la rotación y se resuelve el punto en polígono, con una rejilla de 6°
que reduce las 4.322 divisiones a las pocas candidatas de esa celda.

Los datos van cuantizados a enteros de 16 bits e indexados a 16 bits siempre
que caben, y codificados en base64: 4.322 divisiones (280.000 vértices,
295.000 triángulos) ocupan 5,2 MB y toda la geografía física, 1,2 MB más.

## Comprobaciones

- Las fronteras compartidas coinciden vértice a vértice: ninguna grieta entre
  divisiones vecinas.
- **Fronteras**: los 249 países tienen contorno —ninguno se queda sin—, no hay
  ningún tramo sin país al que atribuirlo, y las 169 listas de vecinos son
  simétricas: si A limita con B, B limita con A. Contrastadas a mano: España →
  Andorra, Francia, Gibraltar, Marruecos, Portugal; Bolivia → Argentina,
  Brasil, Chile, Paraguay, Perú; Mónaco → Francia; San Marino → Italia;
  Islandia → ninguno, solo costa.
- El relleno no se sale del polígono en ninguna división salvo restos por
  debajo del 4% en 68 municipios diminutos (comunas eslovenas, distritos de
  Londres), invisibles a cualquier escala.
- Pinchando en el centro de la pantalla sobre el punto representativo de cada
  división, **4.315 de 4.322** devuelven la división correcta; las 7 restantes
  son franjas de menos de un kilómetro de ancho.
- Pinchando sobre el Himalaya, el Sahara, la cuenca del Amazonas, el Gobi, el
  Baikal y los Andes se obtiene en cada caso el accidente correcto con su
  cumbre: Himalaya → Everest 8.848 m, Andes → Aconcagua 6.959 m, Alpes →
  Mont Blanc 4.807 m, Rocosas → Monte Elbert 4.402 m.
- **Campaña**: la rejilla de celdas reproduce las superficies reales con un
  error del 1% en los países comprobados. Una partida automática desde Viena
  pasa de 37 a 142.154 celdas en 265 turnos, formando bolsas y cercos por el
  camino. Entrar, elegir el punto de partida tocando el mapa, señalar objetivo,
  lanzar la ofensiva, terminar turno, plegar el panel y salir funcionan con el
  dedo, y salir deja el mapa como estaba.
- **Banderas**: los 249 países tienen una, y las 249 se dibujan sin fallar.
- La campaña no toca los ajustes del mapa: el relieve, las divisiones y las
  ciudades siguen como estuvieran, y al terminar no queda nada encendido.
- **Toque**: un toque con hasta 16 px de temblor selecciona; un arrastre de 40
  no. Antes se sumaba el recorrido entero del dedo y cinco eventos de un píxel
  ya contaban como arrastre, así que en una pantalla táctil no había forma de
  tocar nada. La costa se clasifica bien en los 30 países
  comprobados, y las travesías dan 86 km entre Japón y Corea, 122 entre el
  Reino Unido y Francia y 154 entre Cuba y Estados Unidos.
- **Ciudades**: pinchando encima de 40 puntos de ciudad dibujados, 39
  devuelven esa misma ciudad. El que falla siempre es un par de capitales
  pegadas —Kinsasa y Brazzaville, a 5 km una de otra a cada orilla del Congo;
  Roma y la Ciudad del Vaticano, a 2 km—: desde el espacio sus puntos caen a
  menos de 20 píxeles y gana el más cercano al cursor. Acercándose se separan.
  La región sale con el nombre en español del propio mapa en 6.610 de las 7.222
  ciudades que la traen, y en 235 de los 249 países la ficha da su capital.
- **Ríos**: de una lista de 125 grandes ríos del mundo, los 125 están en el
  mapa y con el nombre en español. Ningún nombre queda con caracteres rotos.
  Los 1.057 ríos con nombre son buscables, aunque su rótulo solo aparezca al
  acercarse.
- En los microestados recuperados la superficie es solo orientativa: la rejilla
  de cuantización mide ~930 m, así que Mónaco sale con 18 km² frente a sus 2
  reales. San Marino (61 km²), Anguila (86 frente a 91) o Nauru (30 frente a
  21) quedan más cerca. Sus contornos y sus vecinos sí son correctos.
- Superficies contrastadas con las reales: España 506.716 km² (505.990),
  Italia 301.173 (301.340), Reino Unido 242.553 (242.495), Brasil 8.519.258
  (8.515.767), Japón 375.652 (377.975). Francia suma 636.524 km² porque
  Natural Earth incluye sus departamentos de ultramar.

## Datos

- Divisiones: [Natural Earth](https://www.naturalearthdata.com/), capa
  `ne_10m_admin_1_states_provinces`, dominio público. Los nombres en español
  vienen del propio conjunto de datos (`name_es`).
- Ciudades: Natural Earth, capa `populated_places` (1:10 M), con los nombres
  en español del propio conjunto de datos (`NAME_ES`). La población es el
  máximo del área metropolitana (`POP_MAX`), de en torno a 2010-2015: son
  cifras de aglomeración, no del municipio, y por eso Madrid sale con 5,6
  millones y no con 3,3.
- Geografía física: Natural Earth, capas `geography_regions_polys`,
  `geography_regions_elevation_points`, `geography_regions_points`,
  `rivers_lake_centerlines` y `lakes` (1:10 M) y `glaciated_areas` (1:50 M).
  También en dominio público y también con los nombres en español.
- Países sin divisiones y nombres de país:
  [`johan/world.geo.json`](https://github.com/johan/world.geo.json), derivado
  de Natural Earth 1:110 M, dominio público (`data/LICENSE-countries-geo-json`).

**Sobre los ríos**: la capa de Natural Earth a 1:10 M contiene los ríos
principales del mundo —1.455 trazados, 1.057 con nombre—, no todos los cursos
de agua del planeta. Faltan cauces secundarios; comprobando una lista de 125
grandes ríos, el único ausente del conjunto de datos era el Murrumbidgee
australiano. Un inventario realmente completo (HydroRIVERS, con 8,5 millones de
tramos) ocupa cerca de un gigabyte y no cabe en un archivo HTML.

**Sobre las capitales añadidas a mano**: 16 territorios pequeños no tienen
ninguna ciudad en la capa de Natural Earth, o la que tienen no es su capital.
Se añaden en `tools/build_ciudades.py` (la tabla `CAPITALES_EXTRA`): El Valle,
Yaren, Adamstown, San Pedro, Kingston, Saint Helier, Saint Peter Port, Road
Town, Brades, Jamestown, Philipsburg, Marigot, Gustavia, Mata Utu, Nicosia
Norte y Charlotte Amalie. Las cuatro primeras usan el punto de rótulo que
Natural Earth da a la división administrativa homónima; el resto lleva la
posición del centro urbano puesta a mano, con precisión de unos cientos de
metros. Van marcadas en los datos para poder distinguirlas del origen.

El nivel administrativo 1 no tiene la misma granularidad en todo el mundo: son
las 51 provincias de España, los 50 estados de Estados Unidos, los 27 estados
de Brasil… pero también las 110 provincias de Italia o los 224 distritos del
Reino Unido, que es como Natural Earth los publica. Las superficies son
aproximadas (±2%) por la simplificación, y las fronteras son las del conjunto
de datos de origen.
