#!/usr/bin/env python3
"""Construye data/relieve.json: la geografia fisica del mundo.

Entradas (capas de Natural Earth, ver README)
  data/10m_geography_regions_polys.geojson             cordilleras, desiertos, mesetas...
  data/10m_geography_regions_elevation_points.geojson  cumbres con altitud
  data/10m_geography_regions_points.geojson            cabos, cataratas, polos
  data/10m_rivers_lake_centerlines.geojson             rios
  data/10m_lakes.geojson                               lagos
  data/50m_glaciated_areas.geojson                     hielo permanente

Salida
  data/relieve.json  areas (con relleno), rios (polilineas) y puntos (rotulos)

Los limites de una cordillera o un desierto son indicativos, no administrativos:
se simplifican mucho mas que las fronteras. Los lagos, que si tienen una forma
reconocible, conservan mas detalle.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometria import SCALE, b64_i16, densify_open, pack_polygons, point_in_rings, quantize
from nombres_rios import NOMBRES_RIOS
from topologia import _dp, simplificar

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "relieve.json")

REJILLA = 120.0
MINIMA = 200.0       # km2: por debajo de eso un area no se ve en el globo

# Rejilla del relieve esquematico: 0,5 grados (~55 km) codificada en int8 a
# pasos de 80 m, lo que llega hasta 10.160 m.
CELDA = 0.5
GW = int(360 / CELDA)
GH = int(180 / CELDA)
PASO = 80.0

# Altura por defecto de cada clase, en metros, cuando no hay ninguna cumbre
# dentro del area. Son ordenes de magnitud, no medidas.
ALTURA = {
    "mtn": 2200, "meseta": 1400, "desierto": 400, "llanura": 150,
    "cuenca": 250, "humedal": 40, "tundra": 150, "hielo": 1600, "lago": 0,
}

# Clases de Natural Earth -> clase de dibujo + nombre en espanol.
AREAS = {
    "Range/mtn":  ("mtn", "Cordillera"),
    "Foothills":  ("mtn", "Estribaciones"),
    "Plateau":    ("meseta", "Meseta"),
    "Desert":     ("desierto", "Desierto"),
    "Plain":      ("llanura", "Llanura"),
    "Lowland":    ("llanura", "Tierras bajas"),
    "Basin":      ("cuenca", "Cuenca"),
    "Depression": ("cuenca", "Depresión"),
    "Valley":     ("cuenca", "Valle"),
    "Gorge":      ("cuenca", "Cañón"),
    "Wetlands":   ("humedal", "Humedal"),
    "Delta":      ("humedal", "Delta"),
    "Tundra":     ("tundra", "Tundra"),
}

# Clases que solo aportan un rotulo: su poligono no dice nada que no se vea ya.
PUNTOS_POLY = {
    "Peninsula":    "Península",
    "Pen/cape":     "Península",
    "Isthmus":      "Istmo",
    "Coast":        "Costa",
    "Continent":    "Continente",
    "Geoarea":      "Región",
    "Island group": "Archipiélago",
}

PUNTOS = {
    "mountain":       "Montaña",
    "spot elevation": "Cota",
    "depression":     "Depresión",
    "plateau":        "Meseta",
    "pass":           "Puerto de montaña",
    "cape":           "Cabo",
    "waterfall":      "Catarata",
    "island":         "Isla",
    "island group":   "Archipiélago",
    "plain":          "Llanura",
    "pole":           "Polo",
}


def corrige_paraguay(nom, pts):
    """Separa el rio Paraguay del Parana.

    Natural Earth rotula "Parana" todo el eje, desde el Pantanal hasta el
    estuario, de modo que el Paraguay —uno de los grandes rios de America del
    Sur— no aparece por ninguna parte. La geometria si esta: lo que falta es
    el corte en la confluencia, junto a Corrientes (unos 27,3 S / 58,6 O).
    Aguas arriba de ese punto y al oeste, el cauce es el Paraguay.
    """
    if nom != "Paraná":
        return [(nom, pts)]

    def es_paraguay(q):
        return q[1] > -27.3 and q[0] < -56.0

    trozos = []
    actual = [pts[0]]
    marca = es_paraguay(pts[0])
    for q in pts[1:]:
        m = es_paraguay(q)
        actual.append(q)
        if m != marca:
            trozos.append(("Paraguay" if marca else "Paraná", actual))
            actual = [q]
            marca = m
    trozos.append(("Paraguay" if marca else "Paraná", actual))
    return [(n, t) for n, t in trozos if len(t) >= 2]


def campo(props, clave):
    """Natural Earth alterna mayusculas y minusculas segun la capa."""
    for k in (clave, clave.upper(), clave.lower()):
        v = props.get(k)
        if v not in (None, ""):
            return v
    return None


def nombre(props):
    return (campo(props, "name_es") or campo(props, "name") or
            campo(props, "name_en") or "")


def cargar(fichero):
    ruta = os.path.join(DATA, fichero)
    if not os.path.exists(ruta):
        raise SystemExit("falta %s (ver README)" % ruta)
    with open(ruta, "r", encoding="utf-8") as fh:
        return json.load(fh)


def anillos_de(feature):
    g = feature.get("geometry")
    if not g:
        return []
    if g["type"] == "Polygon":
        return [g["coordinates"]]
    if g["type"] == "MultiPolygon":
        return g["coordinates"]
    return []


def centro_de(anillo):
    xs = [p[0] for p in anillo]
    ys = [p[1] for p in anillo]
    return [round(sum(xs) / len(xs), 3), round(sum(ys) / len(ys), 3)]


def empaqueta_areas(entradas, tol, fraccion, minima=MINIMA):
    """entradas: lista de (nombre, clase, tipo_es, polys). Devuelve areas listas."""
    anillos = []
    plano = []
    for i, (_, _, _, polys) in enumerate(entradas):
        for pi, poly in enumerate(polys):
            for ri, ring in enumerate(poly):
                anillos.append([(float(x), float(y)) for x, y in ring])
                plano.append((i, pi, ri))

    simples, _, _ = simplificar(anillos, q=REJILLA, tol_grados=tol, fraccion=fraccion)

    porentrada = {}
    for (i, pi, ri), simple in zip(plano, simples):
        if simple:
            porentrada.setdefault(i, {}).setdefault(pi, {})[ri] = simple

    salida = []
    for i, (nom, clase, tipo, _) in enumerate(entradas):
        grupos = porentrada.get(i)
        if not grupos:
            continue
        polys = []
        for pi in sorted(grupos):
            aros = grupos[pi]
            if 0 not in aros:
                continue
            polys.append([aros[ri] for ri in sorted(aros)])
        if not polys:
            continue
        packed = pack_polygons(polys)
        if not packed or packed["a"] < minima:
            continue
        salida.append({
            "_anillos": [r for poly in polys for r in poly],
            "n": nom, "cl": clase, "ty": tipo,
            "v": packed["v"], "t": packed["t"], "r": packed["r"],
            "b": packed["b"], "c": packed["c"], "a": packed["a"],
            "i32": packed.get("i32", 0),
        })
    return salida, sum(len(r) for r in anillos), sum(len(r) for r in simples if r)


def rasteriza(areas, puntos):
    """Rejilla de alturas a partir de las areas y las cumbres reales.

    No es un modelo de elevacion: es un relieve esquematico. Cada cordillera
    se levanta hasta la cumbre mas alta que contiene —dato real de Natural
    Earth— y se afila hacia sus bordes, para que no salga una meseta con
    acantilados. Las cumbres anaden su propio pico encima.
    """
    alto = [0.0] * (GW * GH)

    def celdas_de(anillo):
        """Relleno por barrido de un anillo, en coordenadas de rejilla."""
        pts = [((x + 180.0) / CELDA, (y + 90.0) / CELDA) for x, y in anillo]
        ys = [p[1] for p in pts]
        y0 = max(0, int(min(ys)))
        y1 = min(GH - 1, int(max(ys)) + 1)
        n = len(pts)
        for gy in range(y0, y1 + 1):
            yc = gy + 0.5
            cortes = []
            for i in range(n):
                x1, ya = pts[i]
                x2, yb = pts[(i + 1) % n]
                if (ya > yc) != (yb > yc):
                    cortes.append(x1 + (yc - ya) * (x2 - x1) / (yb - ya))
            cortes.sort()
            for k in range(0, len(cortes) - 1, 2):
                gx0 = max(0, int(cortes[k]))
                gx1 = min(GW - 1, int(cortes[k + 1]) + 1)
                for gx in range(gx0, gx1 + 1):
                    yield gy * GW + gx

    # 1. cada area, a la altura de su base
    for a in areas:
        if a["cl"] == "lago":
            continue
        # La cumbre marca el techo, no el suelo: la base de una cordillera esta
        # bastante mas abajo que su pico, que se anade despues encima.
        h = a["cima"][1] * 0.55 if a.get("cima") else ALTURA.get(a["cl"], 300)
        for anillo in a["_anillos"]:
            for c in celdas_de(anillo):
                if alto[c] < h:
                    alto[c] = h

    # 2. afilado hacia los bordes: dos pasadas de media con los vecinos
    for _ in range(2):
        prev = list(alto)
        for gy in range(GH):
            fila = gy * GW
            for gx in range(GW):
                i = fila + gx
                s_ = prev[i] * 2.0
                w = 2.0
                for dy in (-1, 0, 1):
                    yy = gy + dy
                    if yy < 0 or yy >= GH:
                        continue
                    for dx in (-1, 0, 1):
                        xx = (gx + dx) % GW
                        s_ += prev[yy * GW + xx]
                        w += 1.0
                alto[i] = s_ / w

    # 3. las cumbres, encima de todo
    cumbres = [(p["c"][0], p["c"][1], p.get("e", 0)) for p in puntos if p.get("e", 0) > 0]
    for lon, lat, e in cumbres:
        gx = int((lon + 180.0) / CELDA) % GW
        gy = min(GH - 1, max(0, int((lat + 90.0) / CELDA)))
        for dy in (-1, 0, 1):
            yy = gy + dy
            if yy < 0 or yy >= GH:
                continue
            for dx in (-1, 0, 1):
                xx = (gx + dx) % GW
                v = e if (dx == 0 and dy == 0) else e * 0.72
                i = yy * GW + xx
                if alto[i] < v:
                    alto[i] = v

    datos = bytearray(GW * GH)
    for i, v in enumerate(alto):
        q = int(round(v / PASO))
        datos[i] = max(0, min(255, q))
    return datos


def main():
    areas_in = []
    puntos = []

    # --- regiones fisicas ---------------------------------------------------
    geo = cargar("10m_geography_regions_polys.geojson")
    for f in geo["features"]:
        cls = campo(f["properties"], "featurecla") or ""
        nom = nombre(f["properties"])
        if not nom:
            continue
        polys = anillos_de(f)
        if not polys:
            continue
        if cls in AREAS:
            clase, tipo = AREAS[cls]
            areas_in.append((nom, clase, tipo, polys))
        elif cls in PUNTOS_POLY:
            # solo el rotulo, en el centro del anillo mayor
            mayor = max((r for poly in polys for r in poly), key=len)
            puntos.append({"n": nom, "ty": PUNTOS_POLY[cls], "cl": "region",
                           "c": centro_de(mayor)})

    # --- glaciares ----------------------------------------------------------
    hielo = cargar("50m_glaciated_areas.geojson")
    for f in hielo["features"]:
        polys = anillos_de(f)
        if polys:
            areas_in.append((nombre(f["properties"]) or "Hielo permanente",
                             "hielo", "Glaciar", polys))

    areas, antes, despues = empaqueta_areas(areas_in, tol=0.05, fraccion=0.04)
    print("regiones y glaciares: %d areas  %d -> %d puntos"
          % (len(areas), antes, despues))

    # --- lagos: conservan mas detalle, su forma se reconoce ------------------
    lagos_in = []
    for f in cargar("10m_lakes.geojson")["features"]:
        polys = anillos_de(f)
        if polys:
            lagos_in.append((nombre(f["properties"]) or "Lago", "lago", "Lago", polys))
    lagos, la, ld = empaqueta_areas(lagos_in, tol=0.012, fraccion=0.015, minima=25.0)
    print("lagos: %d  %d -> %d puntos" % (len(lagos), la, ld))
    areas.extend(lagos)

    # --- rios ---------------------------------------------------------------
    lineas = []
    crudos = 0
    for f in cargar("10m_rivers_lake_centerlines.geojson")["features"]:
        g = f.get("geometry")
        if not g:
            continue
        trozos = [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]
        rank = int(campo(f["properties"], "scalerank") or 8)
        crudo = (campo(f["properties"], "name") or
                 campo(f["properties"], "name_en") or "").strip()
        # La capa de rios no tiene name_es y algunos nombres llegan con los
        # caracteres no ASCII comidos; la tabla arregla las dos cosas.
        nom = NOMBRES_RIOS.get(crudo, crudo)
        for tr in trozos:
            if len(tr) < 2:
                continue
            crudos += len(tr)
            todos = [(float(x), float(y)) for x, y in tr]
            for nom2, pts in corrige_paraguay(nom, todos):
                if len(pts) < 2:
                    continue
                # Un rio secundario no necesita el mismo detalle que el
                # Amazonas: la tolerancia crece con el rango, que es su orden
                # de importancia.
                tol = 0.004 * (1.0 + rank * 0.35)
                idx = _dp(pts, tol * tol)
                lineas.append((nom2, rank, [pts[i] for i in idx]))

    # Ordenados por importancia: el cliente dibuja solo el prefijo que toca
    # segun el zoom, sin tener que filtrar tramo a tramo.
    lineas.sort(key=lambda t: t[1])
    verts = []
    tramos = []
    cortes = [0] * 12          # primer tramo de cada rango
    rango_ant = -1
    nombres_rio = {}
    for nom, rank, pts in lineas:
        densa = densify_open(pts)
        if len(densa) < 2:
            continue
        while rango_ant < rank:
            rango_ant += 1
            cortes[rango_ant] = len(tramos)
        tramos.append((len(verts) // 2, len(densa)))
        for lon, lat in densa:
            verts.append(quantize(lon, -32767, 32767))
            verts.append(quantize(lat, -32767, 32767))
        if nom and (nom not in nombres_rio or len(pts) > nombres_rio[nom][1]):
            nombres_rio[nom] = (pts[len(pts) // 2], len(pts), rank)
    while rango_ant < 11:
        rango_ant += 1
        cortes[rango_ant] = len(tramos)

    rios = {"v": b64_i16(verts), "s": [x for t in tramos for x in t], "c": cortes}
    print("rios: %d tramos  %d -> %d puntos  cortes=%s"
          % (len(tramos), crudos, len(verts) // 2, cortes))

    # Todos los rios con nombre entran como puntos: asi son buscables aunque
    # su rotulo solo aparezca al acercarse. El rango viaja con ellos.
    for nom, (pt, largo, rank) in nombres_rio.items():
        puntos.append({"n": nom, "ty": "Río", "cl": "rio", "rk": rank,
                       "c": [round(pt[0], 3), round(pt[1], 3)], "e": 0})

    # --- cumbres y otros puntos --------------------------------------------
    for fichero in ("10m_geography_regions_elevation_points.geojson",
                    "10m_geography_regions_points.geojson"):
        for f in cargar(fichero)["features"]:
            g = f.get("geometry")
            if not g or g["type"] != "Point":
                continue
            p = f["properties"]
            nom = nombre(p)
            if not nom:
                continue
            cls = (campo(p, "featurecla") or "").lower()
            elev = campo(p, "elevation")
            lon, lat = g["coordinates"][0], g["coordinates"][1]
            puntos.append({
                "n": nom, "ty": PUNTOS.get(cls, cls.capitalize() or "Punto"),
                "cl": "cumbre" if cls == "mountain" else "punto",
                "c": [round(float(lon), 3), round(float(lat), 3)],
                "e": int(elev) if elev else 0,
            })

    def peso(p):
        # las cumbres por altitud; los rios por su rango; el resto, en medio
        if p.get("e"):
            return p["e"]
        if p.get("cl") == "rio":
            return 6000 - p.get("rk", 8) * 550
        return 1500

    puntos.sort(key=lambda p: (-peso(p), p["n"]))
    areas.sort(key=lambda a: -a["a"])

    # Cumbre más alta de cada área: se comprueba con el polígono, no con su
    # caja. Con la caja, la cuenca del Amazonas heredaba la altura de los Andes.
    cumbres = [p for p in puntos if p.get("e", 0) > 0]
    for a in areas:
        if a["cl"] == "lago":
            continue
        b = a["b"]
        mejor = None
        for p in cumbres:
            lon, lat = p["c"]
            if not (b[0] <= lon <= b[2] and b[1] <= lat <= b[3]):
                continue
            if mejor and p["e"] <= mejor["e"]:
                continue
            if point_in_rings(a["_anillos"], lon, lat):
                mejor = p
        if mejor:
            a["cima"] = [mejor["n"], mejor["e"]]

    import base64
    rejilla = rasteriza(areas, puntos)
    for a in areas:
        a.pop("_anillos", None)

    salida = {"scale": SCALE, "areas": areas, "rios": rios, "puntos": puntos,
              "alturas": {"w": GW, "h": GH, "paso": PASO,
                          "v": base64.b64encode(bytes(rejilla)).decode("ascii")}}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(salida, fh, separators=(",", ":"), ensure_ascii=False)

    from collections import Counter
    print("puntos: %d  %s" % (len(puntos), dict(Counter(p["ty"] for p in puntos).most_common(6))))
    print("areas por clase: %s" % dict(Counter(a["cl"] for a in areas)))
    picos = sum(1 for v in rejilla if v > 25)
    print("rejilla de alturas: %dx%d  celdas sobre 2.000 m: %d" % (GW, GH, picos))
    print("salida: %.0f KB" % (os.path.getsize(OUT) / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
