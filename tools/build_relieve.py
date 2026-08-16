#!/usr/bin/env python3
"""Construye data/relieve.json: la geografia fisica del mundo.

Entradas (capas de Natural Earth, ver README)
  data/10m_geography_regions_polys.geojson             cordilleras, desiertos, mesetas...
  data/10m_geography_regions_elevation_points.geojson  cumbres con altitud
  data/10m_geography_regions_points.geojson            cabos, cataratas, polos
  data/50m_rivers_lake_centerlines.geojson             rios
  data/50m_lakes.geojson                               lagos
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
from geometria import SCALE, b64_i16, densify_open, pack_polygons, quantize
from topologia import simplificar

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "relieve.json")

REJILLA = 120.0
MINIMA = 200.0       # km2: por debajo de eso un area no se ve en el globo

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


def empaqueta_areas(entradas, tol, fraccion):
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
        if not packed or packed["a"] < MINIMA:
            continue
        salida.append({
            "n": nom, "cl": clase, "ty": tipo,
            "v": packed["v"], "t": packed["t"], "r": packed["r"],
            "b": packed["b"], "c": packed["c"], "a": packed["a"],
            "i32": packed.get("i32", 0),
        })
    return salida, sum(len(r) for r in anillos), sum(len(r) for r in simples if r)


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
    for f in cargar("50m_lakes.geojson")["features"]:
        polys = anillos_de(f)
        if polys:
            lagos_in.append((nombre(f["properties"]) or "Lago", "lago", "Lago", polys))
    lagos, la, ld = empaqueta_areas(lagos_in, tol=0.02, fraccion=0.02)
    print("lagos: %d  %d -> %d puntos" % (len(lagos), la, ld))
    areas.extend(lagos)

    # --- rios ---------------------------------------------------------------
    lineas = []
    for f in cargar("50m_rivers_lake_centerlines.geojson")["features"]:
        g = f.get("geometry")
        if not g:
            continue
        trozos = [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]
        rank = campo(f["properties"], "scalerank") or 8
        nom = nombre(f["properties"]) or ""
        for tr in trozos:
            if len(tr) >= 2:
                lineas.append((nom, int(rank), [(float(x), float(y)) for x, y in tr]))

    verts = []
    tramos = []
    rangos = []
    for nom, rank, pts in lineas:
        densa = densify_open(pts)
        if len(densa) < 2:
            continue
        tramos.append((len(verts) // 2, len(densa)))
        rangos.append(rank)
        for lon, lat in densa:
            verts.append(quantize(lon, -32767, 32767))
            verts.append(quantize(lat, -32767, 32767))
    rios = {"v": b64_i16(verts), "s": [x for t in tramos for x in t], "rk": rangos}
    print("rios: %d tramos  %d puntos" % (len(tramos), len(verts) // 2))

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

    puntos.sort(key=lambda p: (-p.get("e", 0), p["n"]))
    areas.sort(key=lambda a: -a["a"])

    salida = {"scale": SCALE, "areas": areas, "rios": rios, "puntos": puntos}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(salida, fh, separators=(",", ":"), ensure_ascii=False)

    from collections import Counter
    print("puntos: %d  %s" % (len(puntos), dict(Counter(p["ty"] for p in puntos).most_common(6))))
    print("areas por clase: %s" % dict(Counter(a["cl"] for a in areas)))
    print("salida: %.0f KB" % (os.path.getsize(OUT) / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
