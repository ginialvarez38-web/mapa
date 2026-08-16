#!/usr/bin/env python3
"""Convierte data/countries.geo.json en el blob que consume el globo 3D.

Para cada pais produce:
  - vertices densificados (lon/lat) para que las aristas sigan la curvatura de la esfera
  - triangulos (ear clipping, con puente para el unico hueco del dataset)
  - offsets de anillos para dibujar los contornos
  - bbox y centroide para el buscador y el "volar a"

Los arrays van cuantizados a int16 y codificados en base64 para que el HTML
final siga siendo un solo archivo autocontenido.
"""

import base64
import json
import math
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nombres_es import NOMBRES

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "data", "countries.geo.json")
OUT = os.path.join(ROOT, "data", "world.json")

SCALE = 180.0        # 1/180 grados ~ 620 m de resolucion, entra en int16
MAX_SEG = 1.5        # grados: longitud maxima de arista antes de subdividir
MAX_TRI = 4.0        # grados de arco: aristas mas largas hunden el triangulo en la esfera
EARTH_R = 6371.0     # km, radio medio


# --------------------------------------------------------------------------
# geometria basica
# --------------------------------------------------------------------------

def ring_area(ring):
    """Area con signo (shoelace). Positiva = antihorario."""
    a = 0.0
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        a += x1 * y2 - x2 * y1
    return a / 2.0


def dedupe(ring):
    """Quita el punto de cierre repetido y los duplicados consecutivos."""
    out = []
    for p in ring:
        if not out or abs(p[0] - out[-1][0]) > 1e-9 or abs(p[1] - out[-1][1]) > 1e-9:
            out.append((float(p[0]), float(p[1])))
    while len(out) > 1 and abs(out[0][0] - out[-1][0]) < 1e-9 and abs(out[0][1] - out[-1][1]) < 1e-9:
        out.pop()
    return out


def strip_collinear(ring, eps=1e-12):
    """Elimina vertices que no doblan el trazado.

    Un punto intermedio de un tramo recto no aporta forma y, en cambio, hace
    fallar el recorte de orejas: la oreja que lo tiene como vertice tiene area
    cero y ninguna oreja vecina puede ignorarlo porque cae sobre su arista.
    """
    pts = list(ring)
    changed = True
    while changed and len(pts) > 3:
        changed = False
        out = []
        n = len(pts)
        for i in range(n):
            ax, ay = pts[(i - 1) % n]
            bx, by = pts[i]
            cx, cy = pts[(i + 1) % n]
            cross = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
            if abs(cross) <= eps:
                changed = True
                continue
            out.append((bx, by))
        if len(out) < 3:
            return pts
        pts = out
    return pts


def close_over_pole(ring):
    """Cierra por el polo los anillos que cruzan el antimeridiano.

    La Antartida se guarda como una banda que salta de +180 a -180: cerrada tal
    cual, su ultima arista cruza el mapa entero y corta el resto del contorno,
    y la triangulacion falla. Bajando por el meridiano hasta el polo y volviendo
    por el otro lado el poligono vuelve a ser simple, y ademas cubre el polo,
    que es lo correcto sobre la esfera.

    Devuelve (anillo, puntos_de_costa). Los vertices anadidos van al final, de
    modo que el contorno dibujable son los primeros puntos_de_costa.
    """
    n = len(ring)
    seam = -1
    for i in range(n):
        if abs(ring[(i + 1) % n][0] - ring[i][0]) > 180:
            seam = i
            break
    if seam < 0:
        return ring, n
    rot = ring[seam + 1:] + ring[:seam + 1]
    pole = -90.0 if sum(p[1] for p in ring) / n < 0 else 90.0
    return rot + [(rot[-1][0], pole), (rot[0][0], pole)], len(rot)


def densify(ring):
    """Subdivide las aristas largas: en la esfera una recta en lon/lat no es recta.

    Devuelve los puntos densificados y las posiciones que ocupan en esa lista
    los vertices originales del anillo.
    """
    out = []
    anchors = []
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        anchors.append(len(out))
        out.append((x1, y1))
        d = max(abs(x2 - x1), abs(y2 - y1))
        steps = int(d / MAX_SEG)
        for s in range(1, steps + 1):
            t = s / (steps + 1.0)
            out.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * t))
    return out, anchors


def point_in_triangle(px, py, ax, ay, bx, by, cx, cy):
    d1 = (px - bx) * (ay - by) - (ax - bx) * (py - by)
    d2 = (px - cx) * (by - cy) - (bx - cx) * (py - cy)
    d3 = (px - ax) * (cy - ay) - (cx - ax) * (py - ay)
    neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (neg and pos)


def earcut(points, indices):
    """Ear clipping O(n^2) sobre una lista de indices en orden antihorario."""
    idx = list(indices)
    tris = []
    guard = len(idx) * len(idx) + 64
    while len(idx) > 3 and guard > 0:
        guard -= 1
        n = len(idx)
        cut = -1
        best = None          # mejor candidato por si ninguna oreja sale limpia
        for i in range(n):
            ia, ib, ic = idx[(i - 1) % n], idx[i], idx[(i + 1) % n]
            ax, ay = points[ia]
            bx, by = points[ib]
            cx, cy = points[ic]
            cross = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
            if cross <= 0:            # vertice reflejo: no es oreja
                continue
            blockers = 0
            for j in idx:
                if j in (ia, ib, ic):
                    continue
                px, py = points[j]
                if point_in_triangle(px, py, ax, ay, bx, by, cx, cy):
                    blockers += 1
                    break
            if blockers == 0:
                cut = i
                break
            if best is None or cross > best[1]:
                best = (i, cross)
        if cut < 0:
            # Anillo degenerado (autointersecciones en el origen): se corta por
            # el vertice mas convexo, que es el que menos deforma el resultado.
            if best is None:
                break
            cut = best[0]
        n = len(idx)
        tris.extend((idx[(cut - 1) % n], idx[cut], idx[(cut + 1) % n]))
        del idx[cut]
    if len(idx) == 3:
        tris.extend(idx)
    return tris


def bridge_holes(points, outer, holes):
    """Une cada hueco al anillo exterior con un puente (tecnica estandar de earcut).

    Devuelve una lista de indices que describe un poligono simple equivalente.
    Los indices duplicados apuntan a vertices ya existentes, asi que no hace
    falta anadir vertices nuevos al buffer.
    """
    poly = list(outer)
    for hole in sorted(holes, key=lambda h: -max(points[i][0] for i in h)):
        # vertice del hueco mas a la derecha
        hi = max(range(len(hole)), key=lambda k: points[hole[k]][0])
        hx, hy = points[hole[hi]]
        # vertice del poligono actual mas cercano hacia la derecha
        best, bestd = None, None
        for k, pi in enumerate(poly):
            px, py = points[pi]
            if px < hx:
                continue
            d = (px - hx) ** 2 + (py - hy) ** 2
            if bestd is None or d < bestd:
                best, bestd = k, d
        if best is None:
            best = max(range(len(poly)), key=lambda k: points[poly[k]][0])
        rot = hole[hi:] + hole[:hi]
        poly = poly[:best + 1] + rot + [rot[0]] + poly[best:]
    return poly


def point_in_rings(rings, x, y):
    """Regla par-impar sobre todos los anillos: los huecos se descuentan solos."""
    inside = False
    for ring in rings:
        n = len(ring)
        j = n - 1
        for i in range(n):
            xi, yi = ring[i]
            xj, yj = ring[j]
            if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
                inside = not inside
            j = i
    return inside


def unit_vec(p):
    lon, lat = math.radians(p[0]), math.radians(p[1])
    cl = math.cos(lat)
    return (cl * math.sin(lon), math.sin(lat), cl * math.cos(lon))


def tri_solid_area(a, b, c):
    """Area del triangulo sobre la esfera unidad, en estereorradianes."""
    ax, ay, az = unit_vec(a)
    bx, by, bz = unit_vec(b)
    cx, cy, cz = unit_vec(c)
    ux, uy, uz = bx - ax, by - ay, bz - az
    vx, vy, vz = cx - ax, cy - ay, cz - az
    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx
    return math.sqrt(nx * nx + ny * ny + nz * nz) / 2.0


def arc_len(a, b):
    """Longitud aproximada de la arista en grados de arco sobre la esfera."""
    dy = b[1] - a[1]
    dx = (b[0] - a[0]) * math.cos(math.radians((a[1] + b[1]) * 0.5))
    return math.hypot(dx, dy)


def subdivide(verts, tris, limit=MAX_TRI):
    """Parte los triangulos grandes hasta que sigan la curvatura de la esfera.

    Un triangulo plano que abarca decenas de grados se hunde bajo la superficie;
    con aristas de ~4 grados el error de flecha baja a 6e-4 R.

    El criterio se aplica a la ARISTA, no al triangulo: los dos triangulos que
    comparten una arista toman siempre la misma decision y la malla queda
    conforme. Partir por triangulo dejaba vertices en T -- un lado partido
    contra un lado recto -- y esas grietas se ven como rendijas, sobre todo
    cerca de los polos.
    """
    cache = {}

    def midpoint(i, j):
        key = (i, j) if i < j else (j, i)
        m = cache.get(key)
        if m is None:
            ax, ay = verts[i]
            bx, by = verts[j]
            m = len(verts)
            verts.append(((ax + bx) * 0.5, (ay + by) * 0.5))
            cache[key] = m
        return m

    def too_long(i, j):
        return arc_len(verts[i], verts[j]) > limit

    work = [tuple(tris[i:i + 3]) for i in range(0, len(tris), 3)]
    for _ in range(24):
        out = []
        split = False
        for a, b, c in work:
            e0, e1, e2 = too_long(a, b), too_long(b, c), too_long(c, a)
            count = e0 + e1 + e2
            if count == 0:
                out.append((a, b, c))
                continue
            split = True
            if count == 3:
                m0, m1, m2 = midpoint(a, b), midpoint(b, c), midpoint(c, a)
                out.extend([(a, m0, m2), (m0, b, m1), (m2, m1, c), (m0, m1, m2)])
            elif count == 1:
                if e0:
                    m = midpoint(a, b)
                    out.extend([(a, m, c), (m, b, c)])
                elif e1:
                    m = midpoint(b, c)
                    out.extend([(a, b, m), (a, m, c)])
                else:
                    m = midpoint(c, a)
                    out.extend([(a, b, m), (m, b, c)])
            elif not e2:
                m0, m1 = midpoint(a, b), midpoint(b, c)
                out.extend([(m0, b, m1), (a, m0, m1), (a, m1, c)])
            elif not e0:
                m1, m2 = midpoint(b, c), midpoint(c, a)
                out.extend([(m1, c, m2), (b, m1, m2), (a, b, m2)])
            else:
                m0, m2 = midpoint(a, b), midpoint(c, a)
                out.extend([(a, m0, m2), (m0, b, c), (m0, c, m2)])
        work = out
        if not split:
            break
    return [i for tri in work for i in tri]


# --------------------------------------------------------------------------
# empaquetado
# --------------------------------------------------------------------------

def b64_i16(values):
    return base64.b64encode(struct.pack("<%dh" % len(values), *values)).decode("ascii")


def b64_u32(values):
    return base64.b64encode(struct.pack("<%dI" % len(values), *values)).decode("ascii")


def quantize(v, lo, hi):
    return max(lo, min(hi, int(round(v * SCALE))))


def build():
    with open(SRC, "r", encoding="utf-8") as fh:
        geo = json.load(fh)

    countries = []
    total_v = total_t = 0

    for feature in geo["features"]:
        name_en = feature["properties"].get("name") or feature.get("id") or "?"
        if name_en not in NOMBRES:
            raise SystemExit("falta la traduccion de %r en tools/nombres_es.py" % name_en)
        name = NOMBRES[name_en]
        geom = feature["geometry"]
        polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]

        verts = []          # (lon, lat) densificados, compartidos por relleno y contorno
        ring_offsets = []   # [inicio, longitud] por anillo, para dibujar los bordes
        tris = []
        pick_rings = []     # anillos sin densificar, para el point-in-polygon en CPU

        for poly in polys:
            ring_index = []
            for r, raw in enumerate(poly):
                ring = strip_collinear(dedupe(raw))
                if len(ring) < 3:
                    continue
                ring, coast = close_over_pole(ring)
                pick_rings.append(ring)
                extra = len(ring) - coast          # vertices anadidos en el polo
                # el exterior antihorario, los huecos horarios
                area = ring_area(ring)
                if (r == 0 and area < 0) or (r > 0 and area > 0):
                    ring.reverse()
                    # al invertir, el cierre polar pasa al principio: se rota
                    # para que la costa vuelva a ocupar los primeros vertices
                    ring = ring[extra:] + ring[:extra]
                dense, anchors = densify(ring)
                start = len(verts)
                verts.extend(dense)
                # Solo la costa real se dibuja: el cierre por el polo es artificial.
                if extra:
                    # hasta el ultimo punto de costa: los intermedios que bajan
                    # al polo pertenecen ya al cierre artificial
                    ring_offsets.append((start, anchors[coast - 1] + 1, 0))
                else:
                    ring_offsets.append((start, len(dense), 1))
                # El recorte de orejas trabaja solo sobre los vertices originales:
                # los intermedios son colineales y bloquearian las orejas validas.
                ring_index.append((r, [start + a for a in anchors]))

            if not ring_index:
                continue
            outer = ring_index[0][1]
            holes = [ix for r, ix in ring_index[1:]]
            loop = bridge_holes(verts, outer, holes) if holes else outer
            tris.extend(earcut(verts, loop))

        if not verts or not tris:
            continue

        tris = subdivide(verts, tris)

        lons = [v[0] for v in verts]
        lats = [v[1] for v in verts]
        bbox = [min(lons), min(lats), max(lons), max(lats)]

        # centroide ponderado por area y superficie real sobre la esfera:
        # los triangulos ya son pequenos, asi que la cuerda aproxima bien al casquete
        cx = cy = wsum = 0.0
        steradians = 0.0
        for i in range(0, len(tris), 3):
            a, b, c = verts[tris[i]], verts[tris[i + 1]], verts[tris[i + 2]]
            w = abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) / 2.0
            cx += (a[0] + b[0] + c[0]) / 3.0 * w
            cy += (a[1] + b[1] + c[1]) / 3.0 * w
            wsum += w
            steradians += tri_solid_area(a, b, c)
        if wsum > 0:
            cx /= wsum
            cy /= wsum
        else:
            cx, cy = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2

        # El centroide de un pais alargado o troceado puede caer en el mar
        # (Japon cae en el mar del Japon). En ese caso se usa el centro del
        # triangulo mas grande, que por construccion esta dentro de tierra.
        if not point_in_rings(pick_rings, cx, cy):
            biggest, barea = None, -1.0
            for i in range(0, len(tris), 3):
                a_, b_, c_ = verts[tris[i]], verts[tris[i + 1]], verts[tris[i + 2]]
                ar = abs((b_[0] - a_[0]) * (c_[1] - a_[1]) - (b_[1] - a_[1]) * (c_[0] - a_[0]))
                if ar > barea:
                    barea, biggest = ar, (a_, b_, c_)
            if biggest:
                cx = sum(p[0] for p in biggest) / 3.0
                cy = sum(p[1] for p in biggest) / 3.0
        km2 = steradians * EARTH_R * EARTH_R

        flat = []
        for lon, lat in verts:
            flat.append(quantize(lon, -32767, 32767))
            flat.append(quantize(lat, -32767, 32767))

        countries.append({
            "id": (feature.get("id") or "").replace("-99", "").replace("CS-KM", "XKX") or "—",
            "n": name,
            "en": name_en,
            "v": b64_i16(flat),
            "t": b64_u32(tris),
            "r": [x for off in ring_offsets for x in off],   # [inicio, puntos, cerrado]
            "b": [round(x, 3) for x in bbox],
            "c": [round(cx, 3), round(cy, 3)],
            "a": round(km2),                           # superficie aproximada en km2
            "p": [[[round(x, 3), round(y, 3)] for x, y in ring] for ring in pick_rings],
        })
        total_v += len(verts)
        total_t += len(tris) // 3

    countries.sort(key=lambda c: c["n"])
    out = {"scale": SCALE, "countries": countries}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, separators=(",", ":"), ensure_ascii=False)

    size = os.path.getsize(OUT)
    print("paises: %d  vertices: %d  triangulos: %d  salida: %.0f KB"
          % (len(countries), total_v, total_t, size / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(build())
