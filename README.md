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
- **Campaña**: el botón `Campaña` abre una **simulación operacional de guerra**
  sobre el mapa político de siempre —los colores de cada país, el relieve y las
  ciudades siguen ahí— y sobre una rejilla de **octavo de grado: 1.370.696
  cuadros de tierra de unos 14 km**, que es lo que permite acercarse y leer el
  frente escalón a escalón. Eliges un país y a partir de ahí:

  - **hay un orden de batalla**. Cada bando reparte a sus hombres en formaciones
    de campaña —legiones, huestes, cuerpos o ejércitos, según el siglo, con el
    ancho del frente como techo—, y cada una sostiene su tramo de línea, nivela
    su propio sector, marcha a la velocidad de su época y ataca por su cuenta
    hacia donde le mandas. Como cada una lleva su objetivo, hay varias ofensivas
    a la vez;
  - **el defensor responde**. Tiene sus propios cuerpos, saca al frente las
    guarniciones del interior, se atrinchera y contraataca por donde te ve el
    flanco descolgado o la línea rota;
  - **hay suministro**, repartido desde cada capital por territorio propio. Lo
    que queda cortado se queda sin comer, pierde organización y acaba
    rindiéndose: los cercos no son una regla aparte, salen de aquí;
  - **las unidades se rompen antes de morir**. La organización baja al atacar y
    la rehacen el descanso y los reemplazos; una ofensiva sin relevos culmina
    sola. Y una posición sólo se pierde cuando el que asalta tiene además con
    qué entrar: los números cuentan;
  - **quien cede se retira**, no se evapora: los supervivientes se repliegan a
    la celda de al lado y refuerzan la siguiente línea. Si no hay por dónde
    salir, se rinden enteros —así es como una bolsa se vuelve prisioneros—;
  - **manda el calendario**. El deshielo y el invierno frenan las ofensivas y
    desgastan a la tropa, cada hemisferio va por su lado y el efecto crece con
    la latitud: en el trópico da igual el mes;
  - **los hombres se acaban**. La quinta de cada país sale de su población, se
    llama despacio y se repone con una clase al año; el territorio conquistado
    no da soldados, sólo carreteras;
  - **hay política**. Se empieza en paz: señalar territorio ajeno es declarar la
    guerra. La moral de un país baja con el terreno perdido, con su capital y
    con su ejército, y cuando toca fondo **capitula** y entrega lo que le
    quedaba. Y cuanto más creces, más probable es que el vecino se te eche
    encima antes de que le llegue el turno;
  - **el terreno cuenta**, con los datos del mapa: la altura real, los ríos como
    línea de defensa y las ciudades como plazas fuertes.

  Y todo eso se pelea **en la época que elijas**: ocho, de la Antigüedad a hoy.
  No son ocho dificultades, son ocho guerras distintas —cambian la quinta que
  puede levantar un estado, el tamaño y el nombre de sus formaciones, la marcha
  diaria, el alcance del suministro por tierra y por mar, lo que vale una
  muralla, lo deprisa que se cava, cuánta sangre cuesta un día de combate, si la
  brecha se puede explotar, si la campaña para en invierno, lo que tarda una
  orden en llegar y lo que se sabe del enemigo—. En 1916 una ofensiva gana diez
  celdas en dos años y paga dos bajas por cada una que hace; en 1942 rompe el
  frente y embolsa ejércitos enteros; en el 348 a. C. la campaña se detiene de
  noviembre a marzo.

  Un tic es un día. No hay turnos ni botón de ataque: **se juega tocando el
  mapa** —una bandera tuya, tomas el mando de ese cuerpo; terreno ajeno, ese
  cuerpo ataca hacia allí; terreno tuyo, se traslada; encima de otra formación,
  se funden en una mayor—. Con **`Todos`** la orden va al ejército entero, y el
  índice lateral es el orden de batalla: cada formación con lo que lleva y lo
  que hace, y se toma su mando tocándola. Cada **cuerpo de
  ejército** se dibuja con la bandera de su país y los hombres que tiene, con
  una flecha hacia su objetivo, y una tira arriba dice la fecha, la estación,
  las celdas, los hombres en línea, la organización, la reserva, contra quién
  estás, las bajas de los dos bandos y el último parte.
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
- **Zoom hasta 19 km de altitud**, la escala de un casco urbano: se
  sigue el curso de un río, se reconoce la forma de un lago y se ve entrar a un
  cuerpo de ejército en una plaza celda a celda: 1.270 lagos y 2.442 tramos de río a
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

**3q. Ni banderas con un cero encima ni banderas que no se dejan tocar.**
Dos cosas que se veían en cuanto jugabas un rato.

*Ningún mando sin tramo de frente.* En el índice aparecía de vez en cuando una
formación con «0 hombres · 0 %», y en el mapa su bandera con un cero. No era una
formación deshecha: era un mando al que el reparto de sectores no le había dado
ni una celda —cada celda va al cuerpo más cercano que tenga sitio, y con el cupo
lleno el que llegaba tarde se quedaba a cero—, y a los diez días se le daba por
deshecho y se levantaba otro. En una campaña de doscientos días pasaba **catorce
veces**. Ahora, terminado el reparto, al que se queda vacío se le da tramo **a
costa del vecino más ancho**: se le pasan las celdas de ese vecino más cercanas
a su puesto de mando, que es por donde los dos sectores se tocan. No se inventa
línea, se reparte la que hay, que es lo que hace un cuartel general cuando
encaja un mando nuevo en el frente. La misma campaña, ahora: **una** vez, y por
una razón de verdad —un cuerpo con una celda y diez hombres, que es un cuerpo
gastado, no un fantasma de contabilidad—.

*Y el dedo.* Con un cuerpo ya cogido, el radio de toque de **todas** las
banderas se encogía a la mitad —dieciséis píxeles— para que tocar al lado de la
tuya fuera una orden y no volver a cogerla. El efecto colateral era que pasar el
mando a otra formación pedía una puntería de ratón: a dieciocho píxeles de una
bandera despejada no la cogía. Ahora la regla no es de radio sino de
**proximidad relativa**: el toque pasa a otra formación sólo si su bandera está
más cerca del dedo que la tuya; si lo que tienes más cerca es la tuya, lo que
estás haciendo es mandarla a ese sitio. Las dos cosas funcionan a la vez —coger
la bandera de al lado con el dedo temblón, y dar una orden a diez píxeles de la
propia— sin que una le quite sitio a la otra.

**3p. Mandar el ejército entero, y que la bandera vaya con lo que toma.**
La campaña tenía buena simulación y mal mando: se llevaba de una en una, y el
motor movía formaciones por su cuenta.

*La bandera va en la punta de lanza.* El puesto de mando se ponía en el centro
de su sector, así que la bandera se quedaba atrás mientras el terreno cambiaba
de color solo, unas celdas más allá. Ahora, con orden de atacar, el puesto de
mando se coloca en **la celda de su sector más cercana al objetivo**: la bandera
va donde su cuerpo está mordiendo, celda a celda. Sin orden, vuelve al centro.

*El ejército entero de una vez.* Un botón de **mando general**: con él puesto,
la orden va a todas las formaciones a la vez, y cada una la interpreta desde
donde está —la que tiene enemigo delante ataca, la que no, va a buscarlo—.
Tocar una bandera vuelve a poner esa sola en la mano.

*Y todas las formaciones, a mano.* El índice lateral pasa a ser el **orden de
batalla**: cada formación con sus hombres, su organización y lo que está
haciendo —al ataque, en marcha, sostiene, orden en camino, sin suministro—.
Tocar una toma su mando y vuela hasta ella, que es la única forma de llegar a la
que se te ha quedado en la otra punta del mapa.

*Y tres cosas que el motor hacía a tus espaldas.* Cuando **un** cuerpo tomaba el
punto señalado, los otros trece se quedaban sin orden mirando al frente: se
mandaba al ejército contra un sitio, lo tomaba uno y la ofensiva se paraba sola.
Ahora, si el objetivo ya es tuyo, cada cuerpo **sigue por su propio eje**; en la
prueba, la misma orden pasa de ganar 571 celdas a ganar 2.550. Las formaciones
nuevas se levantaban en el punto del frente más lejano a las demás, que desde
fuera parecía que un cuerpo se hubiera teletransportado: ahora se levantan **en
la capital**, que es donde se instruye a la quinta, y el parte lo dice. Y seis
formaciones aparecían marcadas «sin suministro» estando perfectamente
abastecidas: el suministro tiene un suelo de 0,18 para el territorio conectado y
el aviso saltaba por debajo de 0,2, así que cualquier cuerpo más allá del alcance
—no cortado, sólo lejos— salía en rojo.

**3o. Las ciudades tienen tamaño, y la división deja de retroceder sola.**

*La mancha urbana.* Una ciudad era un punto igual para Tokio que para un pueblo
de tres mil. Ahora, al acercarse, cada una se dibuja con **su superficie**: el
radio sale de la población con exponente 0,42 —la superficie de una ciudad crece
algo menos que su gente, porque el casco se densifica—, así que un pueblo de diez
mil son dos kilómetros, un millón son doce y diez millones, treinta. Poznań sale
con nueve kilómetros de radio, que es lo que mide. La mancha no es un círculo:
se deforma con tres armónicos sacados del propio índice de la ciudad, así que
cada una tiene su forma y siempre la misma, con el casco viejo más denso en el
centro. Aparece sola cuando pasa de dos píxeles y de noche se lee como el
resplandor de las capitales.

*Y el zoom baja a 19 km*, el límite real: el terreno se dibuja sobre una cáscara
a 1,0016 radios y por debajo de eso la cámara se metería dentro del mapa. Las
líneas se comprimen en el hueco que queda entre el suelo y la cámara conservando
su orden.

*La división que retrocedía sola.* Dos causas, y la segunda llevaba tiempo
rompiendo cosas en silencio. La primera: al tomar la celda señalada, el cuerpo se
quedaba **sin orden**, y entonces el puesto de mando se iba solo al centro de su
sector, muchas veces hacia atrás. Ahora, tomado el objetivo, la ofensiva sigue
por el mismo eje —se busca enemigo más allá de lo que se acaba de tomar— y el
puesto de mando no se mueve mientras tenga a alguien delante. La segunda: un
cuerpo anda cuatro celdas al día y la llegada al destino sólo se comprobaba **al
empezar la jornada**; si pisaba el destino a media marcha, los pasos que le
quedaban no encontraban adónde ir y **daban la orden por imposible justo encima
del sitio al que iba**, sin fijarlo. De ahí que un traslado a veces se
deshiciera solo nada más llegar, y que la fusión de dos cuerpos saliera unas
veces sí y otras no. La llegada se comprueba ahora también a media marcha y al
final del día.

*Y una regresión propia*: al recortar el plano lejano para poder bajar tanto,
las estrellas —que están a cuarenta radios— se quedaron fuera del frustum y la
vista nocturna perdió el cielo. Llevan ahora su propia proyección.

**3ñ. Bajar hasta la ciudad, y que quepan todas las banderas.** Dos peticiones
que descubrieron el mismo tipo de límite escrito a mano cuando el zoom no
bajaba de 127 km.

*El tope de altura.* Ahora se puede bajar hasta **38 km** —el campo de visión
son unos treinta kilómetros, una ciudad con su cinturón—, y para eso hubo que
tocar tres cosas que daban por hecho que la cámara nunca estaría tan cerca. El
plano lejano estaba fijo en 100 radios, lo que a esa altura deja una relación
entre planos que ningún buffer de profundidad aguanta: ahora se ajusta a lo que
de verdad puede verse. Las líneas —costa, fronteras, divisiones, ríos,
retícula— se dibujan sobre cáscaras a cuarenta o setenta kilómetros sobre el
terreno para no pelearse con él por la profundidad, y a 38 km de altitud **la
cámara se habría quedado por debajo de las fronteras**: ahora las cáscaras
encogen con la cámara, conservando su orden. Y la exageración del relieve, que
ya se recogía al acercarse, se recoge del todo, porque a ×16 la cámara acaba
dentro de la montaña.

*Y el que de verdad se notaba*: todo lo que se dibuja como marca sobre el globo
—las ciudades, las banderas de los cuerpos, las cumbres— se descartaba con un
`z <= 0.01`, una centésima de radio, **unos sesenta y cuatro kilómetros**. Por
debajo de esa altura desaparecían de golpe, justo cuando más falta hacen: se
podía bajar a ver el terreno conquistado y no había ni una ciudad en pantalla.
Ese umbral va ahora con la altura de la cámara.

*Y las banderas.* Cuando varios cuerpos ocupaban el mismo punto, las que
chocaban **se descartaban**: de cinco formaciones concentradas se veían dos, y
las otras tres no existían para el dedo. Ahora se abren en abanico —cada una con
su cifra, su sitio donde tocarla y un hilo que la ata a su posición de verdad—,
así que se ven todas las que haya. Y si de verdad quieres una sola grande, se la
mandas encima de otra y **se funden**: la mayor absorbe a la menor, hereda su
sector y asciende de escalón —dos cuerpos son un ejército; dos ejércitos, un
grupo de ejércitos—, con el parte dando cuenta de ello. Durante los tres meses
siguientes no se levanta ninguna formación nueva en su lugar: si has
concentrado, es porque querías concentrar.

De paso, una orden de traslado ya no se evapora si el frente se come la celda de
destino mientras el cuerpo marcha: se reapunta a la celda propia más cercana.

**3n. Concentrar sin que el ejército te lo deshaga.** Traer un cuerpo a un
tramo donde ya hay otros dos o tres —que es media doctrina militar— salía mal de
tres maneras distintas, y las tres eran automatismos peleándose con la orden del
jugador.

*El cuerpo llegaba y se le daba por deshecho.* El reparto de la línea era un
castigo blando por sector lleno, aplicado en el orden en que salieran las
celdas: las locales ya estaban repartidas entre los que llevaban allí semanas, y
el recién llegado no cogía ni una. A los diez días sin sector se le daba por
desbordado y **aparecía uno nuevo en la otra punta del país** — eso es
exactamente lo que se ve como «va a la posición y se vuelve a otra frontera».
Ahora cada mando tiene un **cupo** de línea —su parte, con holgura— y la celda
va al más cercano que aún tenga sitio; con el cupo, un cuerpo que llega a un
tramo cubierto le quita su parte a los vecinos, que es lo que pasa de verdad
cuando un ejército mete otro cuerpo en un sector.

*El recolocador lo echaba.* Un cuerpo con orden de atacar se iba solo al tramo
de frente más cercano a su objetivo **que no cubriera ya otro**, con diez celdas
de separación forzada. Eso está bien cuando mandas a todos a la vez contra el
mismo sitio —así se despliegan en línea en vez de amontonarse—, y está mal justo
después de haber traído uno a mano. Ahora un cuerpo sólo busca otro tramo si
donde está **no tiene a quién atacar**, nunca en los días siguientes a una orden
tuya, y la separación forzada baja de diez celdas a seis.

*Y el toque cogía la bandera de al lado.* Para mandar un cuerpo junto a otros
hay que tocar donde están, y ahí lo que hay son banderas: el toque salía como
«cambiar de cuerpo». Ahora, **con un cuerpo ya en la mano el radio de la bandera
se encoge a la mitad**: tocarla de lleno sigue cambiando de mando, y el resto
del mapa es orden.

**3m. Llevar un cuerpo de un frente a otro, y celdas la mitad de grandes.**
Dos cosas que se pedían a la vez y que resultaron ser la misma clase de
problema: el tablero.

*El cuerpo no llegaba nunca.* Para trasladarlo se le daba el destino y cada día
se movía a la celda vecina que más acercara **en línea recta**. Eso funciona en
campo abierto y se encalla en el primer recodo: un golfo, una cordillera, una
lengua de territorio ajeno, y el cuerpo se quedaba clavado dando vueltas en el
mismo sitio. Ahora se busca el camino de verdad —una anchura desde el destino
por territorio propio hasta dar con el cuerpo, con un tope de celdas para que un
destino inalcanzable no cueste el tablero entero— y se anda por él. Y había un
segundo motivo, más tonto: al llegar, el puesto de mando **saltaba** al centro
de su sector, que seguía siendo el de antes, así que deshacía el traslado en
cuanto lo terminaba. Ahora el puesto de mando también anda —una celda al día— y
se queda quieto veinte días donde lo pones. En la prueba, un cuerpo cruza
Alemania de Polonia al Rin, novecientos kilómetros, y sigue allí dos meses
después.

*Las celdas eran demasiado grandes para acercarse.* Se pasa de 0,25° a 0,125°:
de 1440×720 a **2880×1440 celdas**, de 28 a 14 kilómetros de lado, cuatro veces
más resolución de conquista. Con eso el frente se lee al acercarse —los
salientes, los escalones, las bolsas— en vez de aparecer como una escalera de
bloques. Los números de cada época siguen escritos en celdas de cuarto de grado
y se convierten con un factor: las distancias se multiplican por él y los
hombres por celda se dividen por su cuadrado, así que el tablero fino no cambia
el equilibrio de ninguna guerra.

Cuadruplicar las celdas cuesta memoria y tiempo, y hubo que pagarlo en tres
sitios: **las ciudades pasan de un array de una casilla por celda a un mapa**
—son siete mil entre cuatro millones—, lo que de paso quitó un barrido del
tablero entero **en cada fotograma** para rotular las plazas sitiadas; **el
terreno y las plazas fuertes se calculan al vuelo** en vez de guardarse, porque
sólo los mira el combate unas cuantas veces al día; y el parte del índice, que
también recorría el tablero para contar lo tomado de cada país, ahora lleva la
cuenta al día. Con eso, un día de guerra cuesta **7,2 ms** en el navegador de
pruebas por software, abrir la campaña 1,1 s y el conjunto ocupa 149 MB. Donde
no quepa —o donde la GPU no admita una textura de 2.880— se vuelve solo al
tablero de cuarto de grado: mejor celdas gordas que una pantalla en blanco.

**3l. Que la bandera se pueda tocar.** El mando se toma tocando la bandera del
cuerpo, y no funcionaba por dos razones que se tapaban entre sí. La primera: la
bandera se descartaba si su recuadro chocaba con **cualquier** rótulo ya
dibujado —un pueblo, un río, una cumbre—, así que en media Europa central
sencillamente no había bandera que tocar. La segunda: el toque se resolvía
buscando el cuerpo más cercano **a la celda** tocada, y una celda vista desde
lejos ocupa un píxel, de modo que el dedo caía a diez celdas del puesto de mando
y aquello no se leía como «coge este cuerpo» sino como «marcha hasta aquí».

Ahora la bandera de un cuerpo sólo se aparta de otra bandera, nunca de un
rótulo —en campaña el orden de batalla manda sobre los nombres—, y el toque se
resuelve **en la pantalla**, contra el recuadro donde se acaba de dibujar cada
bandera, con 30 píxeles de margen para el dedo y 22 para el ratón. Tocar la
bandera propia toma el mando; la enemiga no se coge, se ataca.

Y había una tercera razón, que sólo se ve mirando la pantalla de un teléfono: la
tira de campaña tenía `max-width: calc(100vw - 360px)`, pensado para dejar sitio
al índice en un escritorio. En 390 píxeles de ancho eso son **treinta píxeles**,
así que sus seis bloques caían uno debajo de otro y salía una columna que tapaba
media pantalla, banderas incluidas. En pantalla estrecha la tira ocupa ahora todo
el ancho, nace plegada —fecha y cuerpo al mando— y se despliega con un botón.

**3k. Ocho épocas, ocho guerras.** El motor ya se comportaba como una guerra,
pero como una guerra de 1942: la única que sabía pelear. La historia militar
lleva tres mil años diciendo que eso cambia, y cambia de maneras que se pueden
poner en números. Cada época es una tabla de coeficientes, y cada coeficiente
sale de algo que está escrito:

| | Antigüedad | Edad Media | Pólvora | Napoleónica | Industrial | Gran Guerra | Mecanizada | Moderna |
|---|---|---|---|---|---|---|---|---|
| año | 350 a. C. | 1200 | 1700 | 1805 | 1870 | 1916 | 1942 | 2000 |
| quinta (% de la población) | 1,0 | 0,8 | 1,5 | 2,5 | 4,0 | 9,0 | 10,0 | 3,0 |
| formación | Legión 15.000 | Hueste 12.000 | Cuerpo 18.000 | Cuerpo 25.000 | Cuerpo 30.000 | Ejército 40.000 | Ejército 60.000 | Cuerpo 35.000 |
| hombres por celda de asalto | 2.600 | 2.200 | 3.400 | 4.200 | 6.500 | 14.000 | 8.500 | 4.500 |
| marcha (celdas/día ≈ 28 km) | 0,72 | 0,70 | 0,80 | 1,15 | 0,95 | 0,75 | 2,00 | 2,60 |
| suministro (celdas) | 12 | 10 | 16 | 20 | 30 | 34 | 46 | 60 |
| travesía marítima (celdas) | 11 | 11 | 12 | 13 | 14 | 15 | 16 | 18 |
| trinchera (×) | 0,15 | 0,20 | 0,35 | 0,30 | 0,55 | 1,10 | 0,70 | 0,60 |
| plaza fuerte (×) | 2,6 | 3,2 | 2,8 | 2,2 | 2,0 | 1,9 | 1,7 | 1,6 |
| Lanchester *k* | 1,00 | 1,02 | 1,08 | 1,12 | 1,20 | 1,25 | 1,35 | 1,45 |
| ritmo de desgaste | 1,9 | 1,5 | 0,7 | 1,5 | 0,85 | 0,45 | 1,0 | 1,5 |
| persecución | 0,55 | 0,45 | 0,32 | 0,45 | 0,28 | **0,12** | 0,50 | 0,55 |
| explotación (celdas) | 2 | 2 | 1 | 2 | 1 | **0** | 3 | 3 |
| cuarteles de invierno | sí | sí | sí | no | no | no | no | no |
| la orden tarda (días) | 6 | 7 | 5 | 4 | 2 | 2 | 1 | 0 |
| fricción | 0,30 | 0,34 | 0,26 | 0,20 | 0,14 | 0,12 | 0,08 | 0,05 |

*De dónde sale cada cosa.*

**El exponente de Lanchester.** Lanchester y Osipov, en 1915, separaron dos
regímenes: la **ley lineal** del combate antiguo —una fila de duelos, donde el
número cuenta uno a uno— y la **ley cuadrática** del fuego dirigido, donde lo
que pesa no es el número sino su cuadrado, porque cada arma puede cambiar de
blanco. En la simulación no se usa el cuadrado a pelo —Dupuy encontró que la
guerra real queda mucho más cerca de la lineal que de la cuadrática—, sino un
exponente que se aplica a la *razón de fuerzas*: 1,00 en la falange y 1,45 con
munición guiada. Es la diferencia entre que concentrar sirva de poco o lo sea
todo.

**El 3 a 1.** La regla de oro de la doctrina —3:1 para asaltar una posición
preparada, 2,5:1 para un ataque de encuentro, 1:1 para contraatacar— aparece
aquí como lo que es: una tendencia, no un umbral. Los ataques con 3:1 salieron
bien en torno al 74% de las veces en los recuentos históricos, y en la
simulación una posición se pierde cuando el defensor se rompe **y** el atacante
tiene con qué entrar; el contraataque enemigo exige 1,35:1 antes de intentarlo.

**Las frontales.** En Austerlitz, cuatro cuerpos de trece mil hombres en diez
kilómetros. En 1916, la doctrina francobritánica daba a una división de 1.500 a
2.500 metros al atacar y el doble al defender. En 1944 el reglamento alemán
daba a una división de 6 a 10 km, y en el frente ruso hubo divisiones cubriendo
cincuenta. De ahí sale la columna de «hombres por celda de asalto», que es lo
que decide cuánto frente puede atacar de verdad un cuerpo.

**Las marchas.** Veinte a treinta y dos kilómetros al día es la marcha normal de
infantería en casi cualquier siglo; más de treinta y dos, marcha forzada. El
ejército de Alejandro se movía entre 11 y 30 km diarios con todo el tren, y una
punta ligera podía hacer 55. Una división de infantería de la Segunda Guerra
hacía de 19 a 24. Un cuerpo acorazado, mucho más. Por eso la marcha va de 0,7 a
2,6 celdas al día.

**La logística.** Van Creveld: el ejército de tracción animal *vive del país*
por el que marcha, porque el forraje pesa el doble que la comida de los hombres
—veinte libras por caballo frente a tres por soldado, con un caballo por cada
cuatro hombres—, y eso le pone un techo a lo lejos que puede ir de su base. El
ferrocarril lo levanta, el camión lo levanta otra vez. De ahí que el alcance del
suministro vaya de 12 a 60 celdas. Y de ahí también que **la distancia degrade
el suministro pero no lo corte**: lo que lo corta es quedarse sin camino a casa,
y eso es una bolsa. Al mar se le da su propio alcance: sin travesías, Roma no
podía sostener Sicilia y Cerdeña, que es lo que sostuvo durante siete siglos.

**La brecha que no se explota.** La columna que más cambia la partida es la de
explotación, y en la Gran Guerra vale cero. Ésa es toda la historia del frente
occidental: se rompía la primera línea y no había con qué seguir, porque el
defensor traía sus reservas en tren y el atacante avanzaba a pie por encima de
su propio bombardeo. La respuesta llegó como **batalla en profundidad** —
Triandafíllov, Tujachevski, Isserson: atacar en toda la profundidad del
dispositivo enemigo a la vez, romper con ejércitos de choque y explotar con
formaciones móviles hasta provocar la parálisis operativa, no la simple ganancia
de terreno—. En la simulación eso son tres celdas de explotación detrás de cada
brecha, y de ahí salen los embolsamientos.

**La persecución.** En una batalla antigua la mayoría de los muertos son del
bando que huye, y de ahí el 0,55; en 1916 el que cede retrocede dos kilómetros
y vuelve a cavar, y de ahí el 0,12. Es la misma cifra que decide si romper el
frente destruye al enemigo o sólo lo empuja.

**El asedio.** Las plazas fuertes valen por tres ejércitos en la Edad Media y
por poco más de uno hoy, y no se toman al asalto: se toman por hambre. La
mayoría de los asedios medievales británicos no pasaban de dos meses, pero
Palermo aguantó diez y Kenilworth ciento setenta y dos días —al rendirse le
quedaba comida para dos—. Aquí no hace falta ninguna regla de asedio: una plaza
cortada del suministro pierde organización y acaba capitulando sola.

**La fricción y la niebla.** Clausewitz: en la guerra todo es muy sencillo, pero
lo más sencillo es difícil. Cada cuerpo tiene una probabilidad de no hacer lo
que se le mandó —del 30% en la Antigüedad al 5% hoy—, las órdenes tardan en
llegar entre seis días y ninguno, y **lo que sabes del enemigo es una
estimación**: las cifras enemigas se dibujan con un «≈» y un error que va del
70% al 12% según lo que veía cada época. Las propias, exactas.

**El aire.** La interdicción aérea no mata al enemigo: le corta la carretera.
Operación Strangle obligó a los alemanes en Italia a emplear a miles de hombres
sólo en reparar puentes y vías. Aquí se lleva un trozo del alcance del
suministro enemigo: nada antes de 1914, un 3% en la Gran Guerra, un 18% en 1942
y un 35% hoy.

**La política de la guerra.** La moral nacional baja con el terreno perdido, con
la capital y con el ejército de campaña, y el aguante depende del siglo: un
reino antiguo se somete cuando pierde su ejército y su plaza principal, un
estado de 1916 pelea hasta que se le acaba el país. Es la diferencia entre la
guerra por batalla decisiva y la guerra total.

**3j. De pintar el frente a mandar un ejército.** La versión anterior ya
simulaba suministro, organización y desgaste, pero seguía teniendo un solo
ejército sin forma: se señalaba un punto y «el frente» empujaba hacia allí.
Poner encima un **orden de batalla** —cuerpos con su sector, su puesto de mando
y sus órdenes— destapó, uno detrás de otro, cinco fallos que sólo se ven
dejando correr la simulación y mirando los números.

*Los cuerpos no cumplían las órdenes.* Se les mandaba atacar Varsovia y ninguno
tenía delante al enemigo: `atac=0` en los once. Al mandarlos todos al mismo
sitio, sus puestos de mando se amontonaban en la misma celda y el reparto de la
línea les tocaba a trozos sueltos por toda Alemania. Ahora cada cuerpo busca el
tramo más cercano al objetivo **que no cubra ya otro**, y la línea se reparte
contando lo que cada uno lleva encima: un ejército que concentra pone a sus
cuerpos uno al lado del otro sobre el eje, no unos encima de otros.

*Ninguna ofensiva rompía nada.* Altura, plaza fuerte y trinchera se multiplicaban
sin tope: una cota atrincherada salía a cinco veces su fuerza y era inexpugnable
con cualquier proporción. Ahora el producto tiene tope, y aparece lo contrario:
una posición atacada **por varios lados a la vez** pierde parte de lo que la
hacía fuerte. Rodear pasa a valer la pena, que es de donde salen las bolsas.

*El que atacaba se apagaba y no volvía.* La organización de una celda que
asaltaba caía a cero y ahí se quedaba para siempre: el descanso no daba ni para
las bajas del día. Faltaba lo evidente —los reemplazos no son sólo hombres, son
unidades de refresco—, así que ahora reponer levanta también la cohesión. Una
ofensiva se sostiene relevando.

*El defensor picaba los puntos flojos.* Con el frente medio a 13.000 hombres por
celda, las que se perdían tenían **1.400 y organización 0,01**: el enemigo iba a
por las celdas quemadas mientras el grueso del ejército miraba desde la de al
lado. Dos reglas lo arreglan: cada cuerpo **nivela su propio sector** todos los
días —con los hombres va la cohesión, y eso es relevar—, y una posición ya no se
pierde ante quien no tiene con qué entrar.

*Faltaba un millón y medio de hombres.* Cada celda tomada borraba del mundo a su
guarnición. Ahora **quien cede se retira** a la celda de al lado dejando uno de
cada cinco, y si está rodeado se rinde entero: la bolsa se convierte en
prisioneros y las cuentas cuadran.

Con todo junto, una invasión de Polonia se comporta como se espera de una: 70
celdas el primer trimestre, 250 al segundo año, 1,6 bajas propias por cada una
enemiga, ofensivas que culminan en invierno y se reanudan en primavera, y —en
una de las partidas de prueba— nueve países en guerra contigo al cuarto año
porque el vecindario no se queda mirando.

**3i. Que la guerra se comporte como una guerra.** Las tres primeras versiones
jugables eran mapas de pintar casillas: el enemigo no existía. Al ponerlo a
simular de verdad, cada regla que faltaba se vio en los números.

*El mundo caía en cuatro meses.* Los reemplazos salían del territorio ocupado,
así que cada conquista pagaba la siguiente: 338.200 celdas en 120 días. Ahora
los hombres salen de la quinta de **tu** país, es finita y se repone despacio;
una población conquistada no te da soldados.

*El mundo entero se rendía solo.* El suministro sólo se calcula para los países
que tocan al frente, y los demás se quedaban a cero, es decir, dados por
cercados: 200.000 celdas capitulando en dos meses sin que nadie las atacara.
Ahora quien no está en contacto está abastecido, y al perder el contacto se le
devuelve el suministro.

*Dos años sin mover el frente.* Con los refuerzos repartidos a partes iguales
por toda la línea no había superioridad local en ninguna parte, y las ofensivas
culminaban justo antes de romper al defensor. Ahora los refuerzos se concentran
donde señalas, atrincherarse ya no multiplica por 2,4 sino por 1,9, aplastar a
alguien no agota al atacante como pelear de igual a igual, y al ceder una celda
las de al lado pierden cohesión —el flanco al aire— para que un frente se
desmorone en cadena en vez de resistir celda a celda eternamente.

*Empezabas conquistando tu propio país.* La partida arrancaba con una sola
división; ahora arranca con el país entero, que es lo que significa elegir con
quién vas a la guerra. Y el defensor no contraataca las primeras semanas:
quien ataca por sorpresa tiene la iniciativa mientras el otro moviliza.

Con eso, una ofensiva austríaca hacia el Adriático se comporta como se espera:
avanza deprisa el primer mes, culmina hacia el día 240 con la organización por
debajo del 50%, paga dos bajas por cada una que hace atacando posiciones
preparadas, y se para cuando se acaban los hombres.

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
  error del 1% en los países comprobados. Entrar, elegir país tocando el mapa,
  tomar el mando de un cuerpo tocando su bandera, mandarlo a atacar o a
  trasladarse y salir funcionan con el dedo, y salir deja el mapa como estaba.
- **Guerra**: una invasión de Polonia desde Alemania —once cuerpos, eje único,
  objetivos renovados cada mes— pasa de 741 a 1.202 celdas en cuatro años:
  71 celdas polacas el primer trimestre, 247 al segundo año, moral polaca del
  95% al 74%, 1,8 millones de bajas propias por 948.000 ajenas, ofensivas que
  culminan en invierno y se reanudan en primavera, ciudades que caen y se
  recuperan —Poznań, Breslavia—, bolsas sin suministro y prisioneros. Al cuarto
  año hay nueve países en guerra contigo: Francia, Italia, Austria, Bélgica,
  Países Bajos, Dinamarca, Suiza, Luxemburgo y Polonia. En otra partida, Polonia
  capitula hacia el día 900 y entrega lo que le quedaba.
- **Simulación**: sobre el tablero fino de 4,1 millones de celdas, un día de
  guerra cuesta **7,2 ms** en el navegador de pruebas por software, el parte del
  índice 0 ms y un fotograma 14 ms; abrir la campaña, 1,1 s —rasterizar el mundo
  y calcular las travesías marítimas—, y el conjunto ocupa 149 MB.
- **Traslados**: un cuerpo puesto en el frente polaco recibe orden de ir al Rin,
  cruza Alemania entera —de 20,6° E a 7,8° E, unos mil kilómetros— y sigue allí
  dos meses después.
- **Concentración**: con cuatro cuerpos ya juntos en el frente polaco, se toma el
  mando de uno que está en la frontera del oeste tocando su bandera, se le manda
  al grupo tocando junto a la suya, marcha de 6,2° E a 16,1° E, se queda con un
  sector de 24 celdas allí y sigue en su sitio 140 días después.
- **Banderas**: con cinco formaciones concentradas en el mismo punto se dibujan
  las catorce del ejército sin que ninguna tape a otra —cero pares encimados—, y
  siguen apareciendo con la cámara a veinte kilómetros del suelo.
- **Mando**: el índice lista las catorce formaciones; tocar una toma su mando;
  con `Todos` las catorce reciben la misma orden y las catorce la conservan cien
  días después, sin ninguna marcada falsamente sin suministro; tocar una bandera
  devuelve el mando a esa sola.
- **Fusión**: mandar una formación encima de otra las funde —«el XI Ejército se
  funde en el V Ejército»—, la superviviente hereda su sector y asciende de
  escalón.
- **Toque**: tocar la bandera de otra formación le pasa el mando aunque el dedo
  caiga 18 px del centro, y tocar a 10 px de la bandera del cuerpo que ya llevas
  no se lo quita: se le da la orden y sigue siendo el mismo cuerpo el que manda.
- **Sin fantasmas**: en doscientos días de campaña, ninguna formación se queda
  sin sector; antes eran catorce días con una formación a «0 hombres · 0 %» en
  el índice y su bandera con un cero en el mapa.
- **Zoom**: a 19 km de altitud siguen dibujándose las ciudades, las banderas y
  las cumbres; antes, por debajo de 64 km desaparecían todas de golpe.
- **Ciudades**: al acercarse, cada una se dibuja con la superficie que le da su
  población —Poznań, nueve kilómetros de radio—, y la vista nocturna conserva
  sus estrellas.
- **Épocas**: la misma invasión, con la misma orden y el mismo eje, en las ocho.
  Dos años de guerra, desde 741 celdas:

  | época | celdas | tomadas / perdidas | bajas propias / ajenas | invierno |
  |---|---|---|---|---|
  | Antigüedad | 1.369 | +431 / −58 | 352k / 96k | 152 d parados |
  | Edad Media | 1.351 | +375 / −0 | 123k / 56k | 152 d parados |
  | Pólvora | 1.553 | +632 / −34 | 227k / 165k | 152 d parados |
  | Napoleónica | 1.050 | +455 / −146 | 623k / 351k | — |
  | Industrial | 1.000 | +365 / −106 | 481k / 397k | — |
  | Gran Guerra | 857 | **+161 / −45** | **329k / 177k** | — |
  | Mecanizada | 1.331 | +653 / −97 | 733k / 873k | — |
  | Moderna | 1.374 | +581 / −5 | 140k / 904k | — |

  La fila que importa es la de 1916: la ofensiva mejor abastecida y con más
  hombres de todas gana la sexta parte de terreno que las demás y paga dos bajas
  por cada una que hace. Nadie la programó así; sale de que la explotación vale
  cero, la trinchera vale el doble y la persecución no existe. Y la de 2000, al
  revés: poco terreno los primeros meses y una proporción de bajas de uno a seis.
- **Suministro marítimo**: sin travesías, las 39 celdas de Sicilia y Cerdeña
  salían siempre sin abastecer en una campaña italiana. Con ellas, queda una:
  un islote suelto en mitad del Atlántico.
- **Banderas**: los 249 países tienen una, y las 249 se dibujan sin fallar.
- La campaña no toca los ajustes del mapa: el relieve, las divisiones y las
  ciudades siguen como estuvieran, y al terminar no queda nada encendido.
- **Toque**: un toque con hasta 16 px de temblor selecciona; un arrastre de 40
  no. En campaña, tocar la bandera de un cuerpo toma su mando: se comprueba
  sobre las catorce banderas de una ofensiva, tocando el centro y tocando a 18
  píxeles de él, y en los dos casos el mando pasa al cuerpo tocado; el toque
  siguiente sobre terreno ajeno sale como orden para ese mismo cuerpo. Antes se sumaba el recorrido entero del dedo y cinco eventos de un píxel
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

## Sobre la guerra · lecturas

Los coeficientes de las ocho épocas no son de oído. Esto es lo que hay detrás:

- **Lanchester y Osipov (1915-16)**, ley lineal y ley cuadrática —
  [Lanchester's laws](https://en.wikipedia.org/wiki/Lanchester%27s_laws) y
  [Lanchester Systems, Naval Postgraduate School](https://faculty.nps.edu/awashburn/Files/Notes/Lanchester.pdf).
- **Trevor N. Dupuy**, el modelo cuantificado del juicio (QJM/TNDM): poder de
  combate = fuerza × factores del entorno × eficacia, y las «verdades» del
  desgaste —el que gana pierde menos que el que pierde, las fuerzas pequeñas se
  desangran más deprisa— en
  [The Dupuy Institute](https://dupuyinstitute.org/2016/06/17/trevor-n-dupuys-combat-attrition-verities/).
- **La regla del 3 a 1** y lo que dicen de ella los recuentos históricos:
  [Trevor Dupuy and the 3-1 Rule](https://dupuyinstitute.org/2016/07/11/trevor-dupuy-and-the-3-1-rule/)
  y [Mastering the Correlation of Forces](https://www.militaryhistoryonline.com/Modern/Correlation).
- **Frontales por época**: Austerlitz y la dispersión creciente en
  [From Complicated to Complex, Modern War Institute](https://mwi.westpoint.edu/from-complicated-to-complex-the-changing-context-of-war/);
  las frontales divisionarias de 1916 en
  [The Evolution of British Infantry Tactics in World War One](https://www.militaryhistoryonline.com/WWI/BritishInfantryInWWI);
  las de 1944 en [Infantry Unit Frontages during WW2](https://balagan.info/infantry-unit-frontages-during-ww2).
- **Marchas**: [How Fast Do Armies Move?, A Collection of Unmitigated Pedantry](https://acoup.blog/2019/10/06/new-acquisitions-how-fast-do-armies-move/).
- **Logística**: Martin van Creveld, *Supplying War: Logistics from Wallenstein
  to Patton* — el ejército de tracción animal vive del país, y las cuentas de
  forraje frente a rancho en
  [The Economics and Logistics of Horse-drawn Armies](https://journals.gold.ac.uk/index.php/bjmh/article/download/1466/1578/1741)
  e [History of Military Logistics](https://www.hgwdavie.com/).
- **Batalla en profundidad**: Triandafíllov, Tujachevski e Isserson en
  [Deep operation](https://en.wikipedia.org/wiki/Deep_operation) y
  [The Evolution of Russian Operational Art](https://archive.smallwarsjournal.com/index.php/jrnl/art/evolution-russian-operational-art).
- **Asedios**: duraciones y rendiciones por hambre en
  [Siege, New World Encyclopedia](https://www.newworldencyclopedia.org/entry/Siege).
- **Interdicción aérea**: [Operation Strangle](https://en.wikipedia.org/wiki/Operation_Strangle_(World_War_II))
  y [Air interdiction](https://military-history.fandom.com/wiki/Air_interdiction).
- **Clausewitz**, la fricción, la niebla y el punto culminante del ataque;
  **Jomini**, las líneas interiores; **Sun Tzu**, evitar la fuerza y buscar el
  vacío. De ellos salen la orden que tarda en llegar, el «≈» de las cifras
  enemigas y que una ofensiva culmine sola.

Nada de esto convierte la campaña en un modelo predictivo: es un juego. Pero
cada número tiene detrás una razón que se puede discutir, que es más de lo que
suele tener un juego de conquistar el mundo.

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
