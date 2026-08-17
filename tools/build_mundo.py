#!/usr/bin/env python3
"""Construye data/mundo.json: el mundo entero a escala 1:10 M, por divisiones.

Entradas
  data/admin1.geojson      ne_10m_admin_1_states_provinces (Natural Earth)
  data/countries.geo.json  solo para los paises sin divisiones
  tools/nombres_es.py      nombres en espanol

Salida
  data/mundo.json  divisiones (relleno + contorno), paises (metadatos
                   agregados) y fronteras de pais como polilineas.

Por que una sola capa: mezclar los contornos de pais a 1:110 M con las
divisiones a 1:10 M dejaba las costas descuadradas, con las provincias
asomando sobre el mar. Aqui toda la geometria sale del mismo origen y las
fronteras de pais se deducen de los arcos: un arco que separa dos divisiones
de paises distintos —o que no tiene division al otro lado, es decir, costa—
es frontera de pais.
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometria import (SCALE, b64_i16, b64_u16, b64_u32, densify_open,
                       pack_polygons, quantize)
from banderas import bandera_de
from nombres_es import ALIAS_NE, NOMBRES, PAISES_NE
from topologia import cuantizar, simplificar

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "data", "admin1.geojson")
PAISES_GEO = os.path.join(ROOT, "data", "countries.geo.json")
OUT = os.path.join(ROOT, "data", "mundo.json")

REJILLA = 120.0      # puntos por grado al cuantizar (~930 m)
TOLERANCIA = 0.030   # grados (~3,3 km) de recorte maximo al simplificar
MINIMA = 20.0        # km2: por debajo de esto la division no se dibuja

# Natural Earth agrupa Gaza y Cisjordania bajo un mismo codigo (PSX) con dos
# nombres distintos, y el mapa de paises usa PSE. Sin esto salian como dos
# paises y la geometria de Cisjordania se dibujaba dos veces, superpuesta.
A3_ES = {"PSX": "Palestina"}
A3_EQ = {"PSE": "PSX"}

TIPOS = {
    "Province": "Provincia", "State": "Estado", "Region": "Región",
    "Department": "Departamento", "District": "Distrito", "County": "Condado",
    "Prefecture": "Prefectura", "Governorate": "Gobernación",
    "Municipality": "Municipio", "Territory": "Territorio",
    "Autonomous Region": "Región autónoma", "Canton": "Cantón",
    "Division": "División", "Oblast": "Óblast", "Republic": "República",
    "Emirate": "Emirato", "Federal District": "Distrito federal",
    "Union Territory": "Territorio de la Unión", "Parish": "Parroquia",
    "Country": "País", "Capital": "Capital", "City": "Ciudad",
}


def limpia_tipo(props):
    t = (props.get("type_es") or "").strip()
    if t:
        return t
    t = (props.get("type") or props.get("type_en") or "").strip()
    return TIPOS.get(t, t)


RADIO = 6371.0       # km


def largo_km(linea):
    """Longitud de una polilinea lon/lat sobre la esfera."""
    total = 0.0
    for i in range(len(linea) - 1):
        x1, y1 = linea[i]
        x2, y2 = linea[i + 1]
        dx = math.radians(x2 - x1) * math.cos(math.radians((y1 + y2) / 2.0))
        dy = math.radians(y2 - y1)
        total += math.hypot(dx, dy)
    return total * RADIO


def nombre_pais(admin, a3, nombres_en):
    """Nombre en espanol del pais al que pertenece una division."""
    if admin in nombres_en:
        return nombres_en[admin]
    alias = ALIAS_NE.get(admin)
    if alias and alias in nombres_en:
        return nombres_en[alias]
    if admin in PAISES_NE:
        return PAISES_NE[admin]
    return admin or a3


def main():
    for ruta in (SRC, PAISES_GEO):
        if not os.path.exists(ruta):
            raise SystemExit("falta %s" % ruta)

    with open(SRC, "r", encoding="utf-8") as fh:
        geo = json.load(fh)
    with open(PAISES_GEO, "r", encoding="utf-8") as fh:
        mundo110 = json.load(fh)

    nombres_en = dict(NOMBRES)

    # --- 1. simplificacion global compartiendo arcos -----------------------
    anillos = []
    plano = []                     # (feature, poligono, anillo) por cada anillo
    for fi, f in enumerate(geo["features"]):
        g = f.get("geometry")
        if not g:
            continue
        polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for pi, poly in enumerate(polys):
            for ri, ring in enumerate(poly):
                anillos.append([(float(x), float(y)) for x, y in ring])
                plano.append((fi, pi, ri))

    origen = sum(len(r) for r in anillos)
    print("anillos: %d  puntos: %d" % (len(anillos), origen))
    simples, usos, arcos = simplificar(anillos, q=REJILLA, tol_grados=TOLERANCIA)
    quedan = sum(len(r) for r in simples if r)
    print("tras simplificar: %d puntos (%.0f%% menos)"
          % (quedan, 100.0 - 100.0 * quedan / origen))

    # --- 2. clasificar cada arco -------------------------------------------
    # Frontera de pais = el arco separa dos paises, o no hay nada al otro lado
    # (costa). Lo demas es frontera interna entre divisiones.
    # La clave de pais es la misma que usa id_pais, para poder traducir despues
    # cada arco al indice del pais al que pertenece.
    paises_por_arco = {}
    usos_por_arco = {}
    for idx, (fi, _, _) in enumerate(plano):
        p = geo["features"][fi]["properties"]
        clave_pais = (p.get("adm0_a3") or "") or (p.get("admin") or "").strip()
        for clave in usos[idx]:
            paises_por_arco.setdefault(clave, set()).add(clave_pais)
            usos_por_arco[clave] = usos_por_arco.get(clave, 0) + 1

    def es_frontera(clave):
        return len(paises_por_arco.get(clave, ())) >= 2 or usos_por_arco.get(clave, 0) <= 1

    def es_terrestre(clave):
        """Frontera con otro pais al otro lado; lo demas es costa o contorno."""
        return len(paises_por_arco.get(clave, ())) >= 2

    # --- 3. registro de paises ---------------------------------------------
    paises = []
    indice_pais = {}

    def id_pais(admin, a3):
        clave = a3 or admin
        if clave not in indice_pais:
            indice_pais[clave] = len(paises)
            paises.append({"n": A3_ES.get(a3) or nombre_pais(admin, a3, nombres_en), "en": admin,
                           "id": a3 or "—", "a": 0, "nd": 0,
                           "b": [180.0, 90.0, -180.0, -90.0], "c": None, "_mayor": -1.0})
        return indice_pais[clave]

    # --- 4. divisiones ------------------------------------------------------
    porfeat = {}
    for (fi, pi, ri), simple in zip(plano, simples):
        if simple:
            porfeat.setdefault(fi, {}).setdefault(pi, {})[ri] = simple

    divisiones = []
    total_v = total_t = 0
    saltadas = 0
    geounits = set()      # gu_a3 de lo ya dibujado, para no repetir territorios
    menudas = {}          # pais -> trozos por debajo del minimo, por si se queda sin nada

    for fi, f in enumerate(geo["features"]):
        grupos = porfeat.get(fi)
        p = f["properties"]
        nombre = (p.get("name_es") or p.get("name") or p.get("name_en") or "").strip()
        if not grupos or not nombre:
            saltadas += 1
            continue

        polys = []
        for pi in sorted(grupos):
            anillos_p = grupos[pi]
            if 0 not in anillos_p:          # sin exterior el poligono no vale
                continue
            polys.append([anillos_p[ri] for ri in sorted(anillos_p)])
        if not polys:
            saltadas += 1
            continue

        a3 = p.get("adm0_a3") or ""
        admin = (p.get("admin") or "").strip()

        packed = pack_polygons(polys)
        if not packed or packed["a"] < MINIMA:
            saltadas += 1
            if packed:
                menudas.setdefault(a3 or admin, (admin, a3, []))[2].extend(polys)
            continue

        ip = id_pais(admin, a3)

        divisiones.append({
            "n": nombre,
            "en": (p.get("name") or "").strip(),
            "ty": limpia_tipo(p),
            "pa": ip,
            "id": (p.get("iso_3166_2") or p.get("code_hasc") or "").strip(),
            "v": packed["v"], "t": packed["t"], "r": packed["r"],
            "b": packed["b"], "c": packed["c"], "a": packed["a"],
            "i32": packed.get("i32", 0),
            "_fi": fi,
        })
        total_v += packed["nv"]
        total_t += packed["nt"]
        geounits.add((p.get("gu_a3") or "").strip())

    # --- 4b. paises que se quedaron sin ninguna division --------------------
    # Monaco, Gibraltar, Anguila o Nauru estan repartidos en distritos de pocos
    # km2: todos caen por debajo del minimo y el pais entero desaparecia del
    # mapa aunque su costa siguiera dibujandose. Aqui vuelven enteros, en una
    # sola pieza y sin pasar por el minimo.
    rescatados = []
    for clave, (admin, a3, polys) in sorted(menudas.items()):
        if clave in indice_pais or not polys:
            continue
        packed = pack_polygons(polys)
        if not packed:
            continue
        ip = id_pais(admin, a3)
        nombre = paises[ip]["n"]
        divisiones.append({
            "n": nombre, "en": admin, "ty": "País", "pa": ip, "id": a3 or "—",
            "v": packed["v"], "t": packed["t"], "r": packed["r"],
            "b": packed["b"], "c": packed["c"], "a": packed["a"],
            "i32": packed.get("i32", 0),
        })
        total_v += packed["nv"]
        total_t += packed["nt"]
        rescatados.append(nombre)
    if rescatados:
        print("paises recuperados enteros (divisiones bajo el minimo): %s"
              % ", ".join(rescatados))

    # --- 5. paises sin divisiones -------------------------------------------
    # Natural Earth cubre 236 paises; los que faltan entran como una division
    # unica, con su propia geometria del mapa de paises.
    # La comparacion va por el nombre en espanol: Natural Earth escribe algunos
    # paises distinto que el mapa de 180 ("S. Sudan" frente a "South Sudan").
    cubiertos = set(paises[d["pa"]]["n"] for d in divisiones)
    cubiertos_a3 = set(paises[d["pa"]]["id"] for d in divisiones)

    sueltos = []
    for f in mundo110["features"]:
        en = f["properties"].get("name") or ""
        a3_110 = (f.get("id") or "").replace("-99", "").replace("CS-KM", "XKX")
        if NOMBRES.get(en, en) in cubiertos or A3_EQ.get(a3_110, a3_110) in cubiertos_a3:
            continue
        # Natural Earth cuelga algunos territorios de su metropoli (la Guayana
        # Francesa figura como Francia). Sin mirar el gu_a3 se dibujarian dos
        # veces, con la costa y la frontera duplicadas encima.
        if a3_110 in geounits:
            continue
        g = f.get("geometry")
        if not g:
            continue
        polys_src = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        polys = []
        for poly in polys_src:
            anillos_p = []
            for ring in poly:
                q = [(x / REJILLA, y / REJILLA) for x, y in cuantizar(ring, REJILLA)]
                if len(q) >= 3:
                    anillos_p.append(q)
            if anillos_p:
                polys.append(anillos_p)
        if not polys:
            continue
        packed = pack_polygons(polys)
        if not packed:
            continue
        a3 = (f.get("id") or "").replace("-99", "").replace("CS-KM", "XKX") or "—"
        ip = id_pais(en, a3)
        paises[ip]["n"] = NOMBRES.get(en, en)
        divisiones.append({
            "n": NOMBRES.get(en, en), "en": en, "ty": "País", "pa": ip, "id": a3,
            "v": packed["v"], "t": packed["t"], "r": packed["r"],
            "b": packed["b"], "c": packed["c"], "a": packed["a"],
            "i32": packed.get("i32", 0),
        })
        total_v += packed["nv"]
        total_t += packed["nt"]
        sueltos.append((NOMBRES.get(en, en), polys, ip))
    if sueltos:
        print("paises sin divisiones anadidos enteros: %s"
              % ", ".join(n for n, _, _ in sueltos))

    # --- 6. agregados por pais ----------------------------------------------
    for d in divisiones:
        pa = paises[d["pa"]]
        pa["a"] += d["a"]
        pa["nd"] += 1
        b, pb = d["b"], pa["b"]
        pa["b"] = [min(pb[0], b[0]), min(pb[1], b[1]), max(pb[2], b[2]), max(pb[3], b[3])]
        if d["a"] > pa["_mayor"]:            # el centro de su division mayor
            pa["_mayor"] = d["a"]
            pa["c"] = d["c"]
    for pa in paises:
        pa.pop("_mayor", None)
        if pa["c"] is None:
            pa["c"] = [(pa["b"][0] + pa["b"][2]) / 2, (pa["b"][1] + pa["b"][3]) / 2]
        pa["b"] = [round(x, 3) for x in pa["b"]]

    # --- 7. fronteras de pais como polilineas -------------------------------
    # Cada tramo lleva su clase —terrestre o costa— y los paises que separa, de
    # modo que el globo pueda pintarlos distinto, resaltar el contorno de un
    # pais entero y decir con quien limita.
    verts = []
    tramos = []            # (inicio, puntos, clase, paisA, paisB)
    limites = {}           # pais -> vecinos
    largos = {}            # pais -> [km de costa, km de frontera terrestre]

    def ips_de(clave):
        salida = []
        for cp in sorted(paises_por_arco.get(clave, ())):
            ip = indice_pais.get(cp)
            if ip is not None and ip not in salida:
                salida.append(ip)
        return salida

    def anota(densa, clase, ips):
        km = largo_km(densa)
        for ip in ips:
            par = largos.setdefault(ip, [0.0, 0.0])
            par[clase] += km
        if clase == 1:
            for a in ips:
                for b in ips:
                    if a != b:
                        limites.setdefault(a, set()).add(b)
        tramos.append((len(verts) // 2, len(densa), clase,
                       ips[0] if ips else -1, ips[1] if len(ips) > 1 else -1))
        for lon, lat in densa:
            verts.append(quantize(lon, -32767, 32767))
            verts.append(quantize(lat, -32767, 32767))

    for clave, linea in arcos.items():
        if not es_frontera(clave) or len(linea) < 2:
            continue
        pts = list(linea)
        if clave[1]:                     # arco cerrado: se cierra sobre si mismo
            pts.append(linea[0])
        densa = densify_open(pts)
        if len(densa) < 2:
            continue
        anota(densa, 1 if es_terrestre(clave) else 0, ips_de(clave))

    # los paises anadidos enteros aportan todo su contorno
    for _, polys, ip in sueltos:
        for poly in polys:
            for ring in poly:
                densa = densify_open(list(ring) + [ring[0]])
                if len(densa) >= 2:
                    anota(densa, 0, [ip])

    # los tramos van agrupados por clase: primero las costas, luego las
    # fronteras terrestres, que se dibujan encima en otro color.
    tramos.sort(key=lambda t: t[2])
    n_costa = sum(1 for t in tramos if t[2] == 0)

    for ip, pa in enumerate(paises):
        pa["lim"] = sorted(limites.get(ip, ()), key=lambda j: paises[j]["n"])
        # La bandera, descrita con franjas y un emblema: a 16 px es lo que se
        # distingue, y 249 imagenes no caben en un archivo que se abre solo.
        bd = bandera_de(pa["id"])
        if bd:
            pa["bd"] = bd

    # Ningun pais deberia quedarse sin contorno; si pasa, es que su geometria no
    # llego a la salida y hay que mirar por que antes de publicar.
    sin_frontera = [pa["n"] for ip, pa in enumerate(paises) if ip not in largos]
    if sin_frontera:
        print("AVISO paises sin contorno: %s" % ", ".join(sin_frontera))
    huerfanos = sum(1 for t in tramos if t[3] < 0)
    if huerfanos:
        print("AVISO tramos sin pais: %d" % huerfanos)

    fronteras = {"v": b64_i16(verts), "s": [x for t in tramos for x in t[:2]],
                 "nc": n_costa}

    # --- 8. vecindad entre divisiones ---------------------------------------
    # El mismo arco compartido que sirve para no dejar grietas dice tambien
    # quien limita con quien: si dos divisiones usan el mismo arco, son
    # vecinas. Sin esto una campana solo puede avanzar pais a pais.
    divisiones.sort(key=lambda d: (paises[d["pa"]]["n"], d["n"]))
    por_fi = {}
    for i, d in enumerate(divisiones):
        if d.get("_fi") is not None:
            por_fi[d["_fi"]] = i

    arcos_de = {}
    for idx, (fi, _, _) in enumerate(plano):
        i = por_fi.get(fi)
        if i is None:
            continue
        for clave in usos[idx]:
            arcos_de.setdefault(clave, set()).add(i)

    vecinos = [set() for _ in divisiones]
    for clave, quienes in arcos_de.items():
        if len(quienes) < 2:
            continue
        lista = sorted(quienes)
        for a in lista:
            for b in lista:
                if a != b:
                    vecinos[a].add(b)

    plano_vec = []
    offsets = [0]
    for v in vecinos:
        plano_vec.extend(sorted(v))
        offsets.append(len(plano_vec))
    vecindad = {"o": b64_u32(offsets), "v": b64_u16(plano_vec)}
    sin_vecinos = sum(1 for v in vecinos if not v)
    print("vecindad de divisiones: %d enlaces, %d sin vecinos"
          % (len(plano_vec) // 2, sin_vecinos))

    for d in divisiones:
        d.pop("_fi", None)

    orden = sorted(range(len(paises)), key=lambda i: paises[i]["n"])
    remap = dict((viejo, nuevo) for nuevo, viejo in enumerate(orden))
    for d in divisiones:
        d["pa"] = remap[d["pa"]]
    paises = [paises[i] for i in orden]
    for pa in paises:
        pa["lim"] = sorted((remap[j] for j in pa["lim"]))
    # el pais de cada tramo, ya con los indices definitivos (65535 = ninguno)
    fronteras["p"] = b64_u16([remap[x] if x >= 0 else 65535
                              for t in tramos for x in t[3:5]])

    salida = {"scale": SCALE, "divisiones": divisiones, "paises": paises,
              "fronteras": fronteras, "vecindad": vecindad}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(salida, fh, separators=(",", ":"), ensure_ascii=False)

    print("divisiones: %d (descartadas %d)  paises: %d" %
          (len(divisiones), saltadas, len(paises)))
    print("vertices: %d  triangulos: %d" % (total_v, total_t))
    print("fronteras: %d tramos (%d de costa, %d terrestres) / %d puntos"
          % (len(tramos), n_costa, len(tramos) - n_costa, len(verts) // 2))
    print("con bandera: %d de %d paises"
          % (sum(1 for pa in paises if pa.get("bd")), len(paises)))
    print("con vecinos declarados: %d paises"
          % sum(1 for pa in paises if pa["lim"]))
    print("salida: %.0f KB" % (os.path.getsize(OUT) / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
