# Atlas Orbital

Un mapa del mundo en 3D: un globo terráqueo que se dibuja con WebGL a partir de
las fronteras reales de 180 países, sin librerías externas y en **un solo
archivo HTML** que funciona abriéndolo con doble clic.

```
index.html      → abre esto en el navegador
```

## Qué hace

- **Globo esférico** con los países rellenos, sus fronteras y el océano
  sombreado, girando con arrastre del ratón (o del dedo) e inercia.
- **Selección de países**: al pasar el cursor se resalta el país y aparece su
  nombre con las coordenadas exactas; al pinchar se abre su ficha con la
  superficie, el punto central, la antípoda y la hora solar del lugar.
- **Índice lateral** con los 180 países y su superficie, con buscador (acepta
  también el nombre en inglés y el código ISO) que centra el globo en el país.
- **Modo día/noche**: ilumina el globo con la posición real del Sol calculada
  para el instante actual, con su terminador y el halo atmosférico encendido
  solo en el limbo iluminado.
- **Dos estilos**: `Noche` (globo sobre fondo estrellado) y `Carta` (aspecto de
  atlas político impreso). Por defecto sigue el tema claro u oscuro del visor.
- **Retícula** de meridianos y paralelos cada 15°.
- Teclado: flechas para girar, `+` / `−` para acercar, `Inicio` para reiniciar
  la vista y `Esc` para cerrar la ficha.

## Cómo se construye

El HTML final se genera en dos pasos, ambos sin dependencias externas:

```bash
python3 tools/build_data.py    # data/countries.geo.json → data/world.json
python3 tools/bundle.py        # plantilla + datos       → index.html
```

| Archivo | Función |
| --- | --- |
| `src/globo.template.html` | La aplicación: estilos, interfaz y el motor WebGL. |
| `tools/build_data.py` | Convierte el GeoJSON en geometría lista para la GPU. |
| `tools/nombres_es.py` | Nombres de los países en español. |
| `tools/bundle.py` | Inyecta los datos en la plantilla. |
| `data/countries.geo.json` | Fronteras de origen (dominio público). |

`data/world.json` es intermedio y se regenera; no está en el repositorio.

## Decisiones técnicas

Dibujar polígonos geográficos sobre una esfera tiene cuatro trampas, y el
generador de datos resuelve una en cada paso:

**1. Triangular el relleno.** Cada anillo se triangula por recorte de orejas
(*ear clipping*), con puente para los huecos —un país dentro de otro, como
Lesoto dentro de Sudáfrica—. El recorte trabaja sobre el trazado limpio: los
puntos colineales se eliminan antes, porque una oreja de área cero no se puede
recortar y bloquea el algoritmo. Sin esa limpieza, ocho países grandes
—Brasil, Rusia, Estados Unidos…— salían con cuñas cruzándolos.

**2. Curvar la geometría.** Un triángulo plano que abarca decenas de grados se
hunde bajo la superficie de la esfera. Los triángulos se subdividen hasta que
ninguna arista supera los 4° de arco, con un criterio aplicado **a la arista y
no al triángulo**: así los dos triángulos que comparten una arista toman la
misma decisión y la malla queda conforme. Con el criterio por triángulo
aparecían vértices en T —un lado partido contra un lado recto— que se ven como
rendijas finas, sobre todo cerca de los polos.

**3. El antimeridiano.** La Antártida se almacena como una banda que salta de
+180° a −180°. Cerrada tal cual, su última arista cruza el mapa entero y corta
el resto del contorno. Se cierra bajando por el meridiano hasta el polo y
volviendo por el otro lado: el polígono vuelve a ser simple y además cubre el
polo, que es lo correcto sobre la esfera. Ese tramo se marca como no dibujable
para que no aparezca una línea artificial sobre el hielo.

**4. Un punto que esté dentro.** El centroide ponderado por área de un país
alargado o troceado puede caer en el mar —el de Japón cae en el mar del Japón—.
Cuando eso ocurre se usa el centro del triángulo más grande, que por
construcción está en tierra. Es el punto que usan la etiqueta y el botón
«Centrar».

En el navegador, toda la geometría vive en dos búferes —un `drawElements` para
los rellenos y otro para las fronteras— y el color de cada país se lee de una
textura-paleta indexada por el atributo de pertenencia, de modo que resaltar un
país es cambiar un uniforme, no reconstruir nada. La selección no usa lectura
de píxeles: se lanza un rayo desde el cursor, se corta con la esfera, se
deshace la rotación y se resuelve el punto en polígono sobre los anillos
originales.

Los datos van cuantizados a enteros de 16 bits (~620 m de resolución) y
codificados en base64 para que el archivo único no se dispare: 180 países,
34 623 vértices y 55 693 triángulos ocupan 1,3 MB.

## Comprobaciones

- El área triangulada de cada polígono coincide con la del polígono de origen
  (desviación máxima 1,2%, en Malta, por el redondeo de la cuantización).
- Las superficies calculadas sobre la esfera concuerdan con las reales:
  España 502 000 km², Francia 558 000 km², Brasil 8,61 M km².
- Pinchando en el centro de la pantalla sobre el punto representativo de cada
  país, los 180 devuelven el país correcto.

## Datos

Fronteras: [`johan/world.geo.json`](https://github.com/johan/world.geo.json),
derivado de Natural Earth (escala 1:110 m), en dominio público. La licencia
original se conserva en `data/LICENSE-countries-geo-json`.

Al ser una simplificación a 1:110 m, las superficies son aproximadas (±2%) y no
aparecen los países más pequeños. Las fronteras son las del conjunto de datos
de origen.
