#!/usr/bin/env python3
"""Construye data/ciudades.json: las capitales y las ciudades del mundo.

Entradas
  data/10m_populated_places.geojson  ne_10m_populated_places (Natural Earth)
  data/mundo.json                    para atar cada ciudad a su pais

Salida
  data/ciudades.json  posiciones, nombres en espanol, poblacion, clase y el
                      rango de importancia con el que aparecen segun el zoom.

Las ciudades van ordenadas por rango, y "cortes" da el indice de la primera de
cada rango: el globo dibuja solo hasta el rango que toque a esa distancia, sin
recorrer las 7.000 en cada fotograma.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometria import SCALE, b64_i16, b64_u16, b64_u32, quantize
from nombres_es import ALIAS_NE, NOMBRES, PAISES_NE

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "data", "10m_populated_places.geojson")
MUNDO = os.path.join(ROOT, "data", "mundo.json")
OUT = os.path.join(ROOT, "data", "ciudades.json")

# Clases: 0 capital de pais, 1 capital regional, 2 ciudad, 3 base cientifica.
# "Admin-0 region capital" es la capital de un territorio dependiente —Nuuk en
# Groenlandia, Papeete en la Polinesia Francesa—: para quien mira el mapa es la
# capital de ese territorio, no una capital de provincia.
CLASES = {
    "Admin-0 capital": 0,
    "Admin-0 capital alt": 0,
    "Admin-0 region capital": 0,
    "Admin-1 capital": 1,
    "Admin-1 region capital": 1,
    "Scientific station": 3,
    "Meteorological Station": 3,
}

# Natural Earth marca Gaza y Ramala como capitales de Palestina; la sede del
# gobierno es Ramala.
CAPITAL_PREFERIDA = {"Palestina": "Ramala"}

# Paises que no estan en el mapa y de los que si hay ciudad.
PAIS_SUELTO = {"Vatican": "Vaticano"}

# Ciudades que Natural Earth trae sin marcar como capital de su territorio.
# Aqui solo se asciende una ciudad que ya existe en el origen.
CAPITAL_ASCENDIDA = {
    "Islas Feroe": "Tórshavn",
}

# Capitales de territorios pequenos que no estan en ne_10m_populated_places.
# Las cuatro primeras salen del propio Natural Earth —son la division
# administrativa homonima de ne_10m_admin_1_states_provinces, con su punto de
# rotulo—; el resto van a mano, con la posicion del centro urbano. Se marcan
# como anadidas para poder distinguirlas del origen.
#   pais, nombre, lon, lat, habitantes (0 = sin dato)
CAPITALES_EXTRA = [
    ("Anguila", "El Valle", -63.0520, 18.2321, 1067, "The Valley"),
    ("Nauru", "Yaren", 166.9250, -0.5432, 803),
    ("Islas Pitcairn", "Adamstown", -130.1020, -25.0707, 40),
    ("San Pedro y Miquelón", "San Pedro", -56.1918, 46.7795, 5400),
    ("Isla Norfolk", "Kingston", 167.9610, -29.0560, 900),
    ("Jersey", "Saint Helier", -2.1070, 49.1870, 33500),
    ("Guernsey", "Saint Peter Port", -2.5360, 49.4550, 18200),
    ("Islas Vírgenes Británicas", "Road Town", -64.6230, 18.4270, 12600),
    ("Montserrat", "Brades", -62.2130, 16.7920, 1000),
    ("Santa Elena", "Jamestown", -5.7170, -15.9280, 630),
    ("Sint Maarten", "Philipsburg", -63.0450, 18.0260, 1300),
    ("San Martín", "Marigot", -63.0830, 18.0700, 5700),
    ("Saint Barthelemy", "Gustavia", -62.8510, 17.8970, 2600),
    ("Wallis y Futuna", "Mata Utu", -176.1760, -13.2820, 1200),
    ("Chipre del Norte", "Nicosia Norte", 33.3650, 35.1830, 61400),
    ("Islas Vírgenes de EE. UU.", "Charlotte Amalie", -64.9310, 18.3419, 14500),
]

NADA = 65535


def rango(cl, pop, capital_regional):
    """Cuando aparece la ciudad: 0 se ve desde el espacio, 9 solo de cerca.

    Las capitales entran siempre las primeras aunque sean diminutas —Palikir
    tiene 4.645 habitantes y sigue siendo una capital—, y por debajo manda la
    poblacion, que es lo que decide el tamano de un rotulo en cualquier atlas.
    """
    if cl == 0:
        return 0
    if pop >= 5000000:
        return 0
    if pop >= 2000000:
        return 1
    if pop >= 1000000:
        return 2
    if pop >= 500000 or (capital_regional and pop >= 200000):
        return 3
    if pop >= 250000 or capital_regional:
        return 4
    if pop >= 100000:
        return 5
    if pop >= 50000:
        return 6
    if pop >= 20000:
        return 7
    if pop >= 5000:
        return 8
    return 9


def main():
    for ruta in (SRC, MUNDO):
        if not os.path.exists(ruta):
            raise SystemExit("falta %s" % ruta)

    with open(SRC, "r", encoding="utf-8") as fh:
        geo = json.load(fh)
    with open(MUNDO, "r", encoding="utf-8") as fh:
        mundo = json.load(fh)

    paises = mundo["paises"]
    # Divisiones por pais, para traducir la region de cada ciudad al nombre en
    # espanol que ya usa el mapa: Natural Earth la escribe en ingles.
    divisiones = mundo["divisiones"]
    div_por_pais = {}
    for i, d in enumerate(divisiones):
        tabla_d = div_por_pais.setdefault(d["pa"], {})
        for clave in (d.get("en"), d.get("n")):
            if clave:
                tabla_d.setdefault(clave.strip().lower(), i)

    por_a3 = {}
    por_nombre = {}
    for i, p in enumerate(paises):
        if p["id"] and p["id"] != "—":
            por_a3.setdefault(p["id"], i)
        por_nombre.setdefault(p["n"], i)

    def id_pais(props):
        a3 = (props.get("ADM0_A3") or "").strip()
        if a3 in por_a3:
            return por_a3[a3]
        sov = (props.get("SOV_A3") or "").strip()
        if sov in por_a3:
            return por_a3[sov]
        en = (props.get("ADM0NAME") or "").strip()
        for nombre in (NOMBRES.get(en), PAISES_NE.get(en),
                       NOMBRES.get(ALIAS_NE.get(en, ""))):
            if nombre and nombre in por_nombre:
                return por_nombre[nombre]
        return None

    ciudades = []
    sin_pais = set()
    for f in geo["features"]:
        g = f.get("geometry")
        if not g or g["type"] != "Point":
            continue
        p = f["properties"]
        nombre = (p.get("NAME_ES") or p.get("NAME") or p.get("NAMEASCII") or "").strip()
        if not nombre:
            continue
        # LONGITUDE/LATITUDE son la posicion del rotulo, no siempre la del
        # punto; la geometria es la buena.
        lon, lat = float(g["coordinates"][0]), float(g["coordinates"][1])
        if not (-180.0 <= lon <= 180.0 and -90.0 <= lat <= 90.0):
            continue
        alias = (p.get("NAME_EN") or p.get("NAME") or "").strip()
        cl = CLASES.get(p.get("FEATURECLA") or "", 2)
        pop = int(p.get("POP_MAX") or 0)
        if pop < 0:                 # Natural Earth escribe -99 cuando no lo sabe
            pop = 0
        ip = id_pais(p)
        en = (p.get("ADM0NAME") or "").strip()
        if ip is None:
            sin_pais.add((en or "?", p.get("ADM0_A3") or "?"))
        ciudades.append({
            "n": nombre,
            "lon": lon, "lat": lat,
            "cl": cl,
            "pop": pop,
            "pa": ip if ip is not None else NADA,
            # el Vaticano no esta en el mapa de paises y su ciudad si: sin esto
            # la ficha se quedaria sin decir donde esta
            "pn": "" if ip is not None else PAIS_SUELTO.get(en, NOMBRES.get(en, en)),
            # el nombre del origen, para que "Munich" o "Cologne" encuentren
            # Múnich y Colonia
            "en": alias if alias != nombre else "",
            # Natural Earth le pone al Vaticano la region italiana que lo rodea:
            # para una ciudad que es su propio pais no dice nada
            "rg": "" if ip is None else (p.get("ADM1NAME") or "").strip(),
            "dv": -1,
            "tz": (p.get("TIMEZONE") or "").strip(),
            "rk": rango(cl, pop, cl == 1),
        })

    # region en espanol: la division del propio mapa cuando se reconoce
    encajadas = 0
    for c in ciudades:
        if c["pa"] == NADA or not c["rg"]:
            continue
        idx = div_por_pais.get(c["pa"], {}).get(c["rg"].lower())
        if idx is not None:
            c["dv"] = idx
            c["rg"] = divisiones[idx]["n"]
            encajadas += 1

    # --- capitales que faltan o que el origen no marca ----------------------
    for pais, ciudad in sorted(CAPITAL_ASCENDIDA.items()):
        ip = por_nombre.get(pais)
        if ip is None:
            print("AVISO: %s no esta en el mapa" % pais)
            continue
        for c in ciudades:
            if c["pa"] == ip and c["n"] == ciudad:
                c["cl"] = 0
                c["rk"] = 0
                break
        else:
            print("AVISO: %s no tiene ciudad %s" % (pais, ciudad))

    anadidas = []
    for fila in CAPITALES_EXTRA:
        pais, nombre, lon, lat, pop = fila[:5]
        alias = fila[5] if len(fila) > 5 else ""
        ip = por_nombre.get(pais)
        if ip is None:
            print("AVISO: %s no esta en el mapa" % pais)
            continue
        if any(c["pa"] == ip and c["cl"] == 0 for c in ciudades):
            continue                      # el origen ya trae capital: manda esa
        ciudades.append({"n": nombre, "lon": lon, "lat": lat, "cl": 0, "pop": pop,
                         "pa": ip, "pn": "", "en": alias, "rg": "", "dv": -1,
                         "tz": "",
                         "rk": 0, "x": 1})
        anadidas.append(nombre)

    # --- capitales de los territorios que no las declaran -------------------
    # Natural Earth no marca capital de pais en las Feroe, las Cook o las
    # Marianas: la unica ciudad suya marcada como capital es su sede. Si hay dos
    # candidatas (Chipre del Norte trae Famagusta y Kyrenia) se deja en blanco
    # antes que arriesgar una respuesta falsa.
    por_pais = {}
    for c in ciudades:
        if c["pa"] != NADA:
            por_pais.setdefault(c["pa"], []).append(c)
    rescatadas = []
    for ip, lista in por_pais.items():
        if any(c["cl"] == 0 for c in lista):
            continue
        cand = [c for c in lista if c["cl"] == 1]
        if len(cand) == 1:
            cand[0]["cl"] = 0
            cand[0]["rk"] = 0
            rescatadas.append(cand[0]["n"])

    # por rango y, dentro de cada uno, por poblacion: el rotulo grande primero
    ciudades.sort(key=lambda c: (c["rk"], -c["pop"], c["n"]))

    cortes = []
    for r in range(11):
        idx = len(ciudades)
        for i, c in enumerate(ciudades):
            if c["rk"] >= r:
                idx = i
                break
        cortes.append(idx)

    # tablas de regiones y husos horarios: se repiten muchisimo
    def tabla(clave):
        vistos = {}
        indices = []
        for c in ciudades:
            v = c[clave]
            if not v:
                indices.append(NADA)
                continue
            if v not in vistos:
                vistos[v] = len(vistos)
            indices.append(vistos[v])
        orden = sorted(vistos, key=lambda k: vistos[k])
        return orden, indices

    regiones, idx_regiones = tabla("rg")
    husos, idx_husos = tabla("tz")

    verts = []
    for c in ciudades:
        verts.append(quantize(c["lon"], -32767, 32767))
        verts.append(quantize(c["lat"], -32767, 32767))

    # la capital de cada pais, para su ficha
    capitales = {}
    for i, c in enumerate(ciudades):
        if c["cl"] != 0 or c["pa"] == NADA:
            continue
        ip = c["pa"]
        preferida = CAPITAL_PREFERIDA.get(paises[ip]["n"])
        if ip in capitales and not (preferida and c["n"] == preferida):
            continue
        capitales[ip] = i

    salida = {
        "scale": SCALE,
        "v": b64_i16(verts),
        "n": [c["n"] for c in ciudades],
        "en": [[i, c["en"]] for i, c in enumerate(ciudades) if c["en"]],
        "cl": b64_u16([c["cl"] for c in ciudades]),
        "pop": b64_u32([c["pop"] for c in ciudades]),
        "pa": b64_u16([c["pa"] for c in ciudades]),
        "rg": b64_u16(idx_regiones),
        "dv": b64_u16([c["dv"] if c["dv"] >= 0 else NADA for c in ciudades]),
        "tz": b64_u16(idx_husos),
        "regiones": regiones,
        "husos": husos,
        "cortes": cortes,
        "capitales": [[k, v] for k, v in sorted(capitales.items())],
        "ajenas": [[i, c["pn"]] for i, c in enumerate(ciudades) if c["pn"]],
        "manual": [i for i, c in enumerate(ciudades) if c.get("x")],
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(salida, fh, separators=(",", ":"), ensure_ascii=False)

    por_clase = {}
    for c in ciudades:
        por_clase[c["cl"]] = por_clase.get(c["cl"], 0) + 1
    print("ciudades: %d  capitales: %d  capitales regionales: %d  bases: %d"
          % (len(ciudades), por_clase.get(0, 0), por_clase.get(1, 0), por_clase.get(3, 0)))
    print("por rango: %s" % {r: cortes[r + 1] - cortes[r] if r + 1 < len(cortes)
                             else len(ciudades) - cortes[r] for r in range(10)})
    print("region en espanol: %d de %d ciudades" %
          (encajadas, sum(1 for c in ciudades if c["rg"])))
    if anadidas:
        print("capitales anadidas a mano (%d): %s" % (len(anadidas), ", ".join(anadidas)))
    print("paises con capital: %d de %d (%d deducidas: %s)"
          % (len(capitales), len(paises), len(rescatadas), ", ".join(sorted(rescatadas))))
    sin_cap = [paises[i]["n"] for i in range(len(paises)) if i not in capitales]
    print("sin capital (%d): %s" % (len(sin_cap), ", ".join(sin_cap)))
    if sin_pais:
        print("AVISO sin pais (%d): %s"
              % (len(sin_pais), ", ".join("%s/%s" % t for t in sorted(sin_pais)[:12])))
    print("salida: %.0f KB" % (os.path.getsize(OUT) / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
