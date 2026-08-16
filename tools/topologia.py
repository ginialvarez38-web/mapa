# -*- coding: utf-8 -*-
"""Simplificacion de poligonos que respeta las fronteras compartidas.

Simplificar cada division por separado abre grietas: dos provincias vecinas
recortan su frontera comun de forma distinta y entre ellas aparece una rendija.
La solucion es la de TopoJSON: cortar todos los anillos en arcos, quedarse con
una sola copia de cada arco compartido, simplificarlo una vez y reconstruir los
anillos con el resultado. Asi las dos vecinas usan exactamente la misma linea.
"""

import math


def cuantizar(ring, q):
    """Redondea a una rejilla de 1/q grados y quita repetidos consecutivos.

    Es el paso que hace comparables los puntos de dos anillos vecinos: sin el,
    dos coordenadas casi iguales no se reconocerian como el mismo vertice.
    """
    out = []
    for x, y in ring:
        p = (int(round(x * q)), int(round(y * q)))
        if not out or p != out[-1]:
            out.append(p)
    while len(out) > 1 and out[0] == out[-1]:
        out.pop()
    return out


def uniones(anillos):
    """Puntos donde cambia la vecindad, es decir, donde se bifurcan las fronteras.

    Un punto interior de una frontera compartida tiene los mismos dos vecinos en
    los dos anillos que la recorren; en un punto triple, no. Esos son los que
    cortan los arcos.
    """
    visto = {}
    junc = set()
    for ring in anillos:
        n = len(ring)
        for i, p in enumerate(ring):
            a = ring[i - 1]
            b = ring[(i + 1) % n]
            par = (a, b) if a <= b else (b, a)
            anterior = visto.get(p)
            if anterior is None:
                visto[p] = par
            elif anterior != par:
                junc.add(p)
    return junc


def cortar(ring, junc):
    """Parte un anillo en arcos por sus uniones. Sin uniones, es un arco cerrado."""
    idx = [i for i, p in enumerate(ring) if p in junc]
    if len(idx) < 2:
        return [(list(ring), True)]
    arcos = []
    for k in range(len(idx)):
        i = idx[k]
        j = idx[(k + 1) % len(idx)]
        seg = ring[i:j + 1] if j > i else ring[i:] + ring[:j + 1]
        if len(seg) >= 2:
            arcos.append((seg, False))
    return arcos


def _dp(pts, tol2):
    """Douglas-Peucker iterativo sobre una polilinea, conservando los extremos."""
    n = len(pts)
    if n < 3:
        return list(range(n))
    keep = [False] * n
    keep[0] = keep[n - 1] = True
    pila = [(0, n - 1)]
    while pila:
        i, j = pila.pop()
        if j - i < 2:
            continue
        ax, ay = pts[i]
        bx, by = pts[j]
        dx, dy = bx - ax, by - ay
        largo2 = dx * dx + dy * dy
        peor, peord = -1, -1.0
        for k in range(i + 1, j):
            px, py = pts[k]
            if largo2 == 0:
                d = (px - ax) ** 2 + (py - ay) ** 2
            else:
                t = ((px - ax) * dx + (py - ay) * dy) / largo2
                t = 0.0 if t < 0 else (1.0 if t > 1 else t)
                ex, ey = ax + t * dx - px, ay + t * dy - py
                d = ex * ex + ey * ey
            if d > peord:
                peord, peor = d, k
        if peord > tol2:
            keep[peor] = True
            pila.append((i, peor))
            pila.append((peor, j))
    return [i for i in range(n) if keep[i]]


def simplificar_arco(seg, cerrado, tol, minimo=4):
    """Simplifica un arco. Los cerrados se parten en dos para no colapsar."""
    tol2 = tol * tol
    if not cerrado:
        idx = _dp(seg, tol2)
        return [seg[i] for i in idx]

    n = len(seg)
    if n <= minimo:
        return list(seg)
    # dos anclas opuestas: el primer punto y el mas lejano a el
    ax, ay = seg[0]
    lejos = max(range(1, n), key=lambda k: (seg[k][0] - ax) ** 2 + (seg[k][1] - ay) ** 2)
    a = seg[:lejos + 1]
    b = seg[lejos:] + [seg[0]]
    pts = [a[i] for i in _dp(a, tol2)] + [b[i] for i in _dp(b, tol2)][1:-1]
    if len(pts) < 3:
        # el anillo se ha quedado en nada: se conserva una version minima
        paso = max(1, n // minimo)
        pts = seg[::paso]
    return pts


def _tolerancia(seg, tol_max, tol_min, fraccion):
    """Tolerancia proporcional al tamano del arco.

    Con una tolerancia fija, una isla de 20 km se convierte en un cuadrilatero
    mientras que una costa de 3.000 km apenas cambia. Midiendo el propio arco,
    cada uno se recorta en la misma proporcion. Depende solo del arco, asi que
    los dos poligonos que lo comparten calculan el mismo valor.
    """
    xs = [p[0] for p in seg]
    ys = [p[1] for p in seg]
    diag = math.hypot(max(xs) - min(xs), max(ys) - min(ys))
    return max(tol_min, min(tol_max, diag * fraccion))


def simplificar(anillos, q=120.0, tol_grados=0.02, tol_min=0.002, fraccion=0.03):
    """Simplifica un conjunto de anillos compartiendo los arcos comunes.

    Recibe y devuelve anillos en grados. `q` es la rejilla de cuantizacion,
    `tol_grados` el recorte maximo y `fraccion` la parte del tamano del arco
    que se admite perder.
    """
    cuant = [cuantizar(r, q) for r in anillos]
    validos = [(i, r) for i, r in enumerate(cuant) if len(r) >= 3]
    junc = uniones([r for _, r in validos])

    cache = {}
    salida = [None] * len(anillos)
    tol_max = tol_grados * q
    tol_piso = tol_min * q

    usos = [[] for _ in anillos]     # arcos que compone cada anillo

    for i, ring in validos:
        piezas = []
        for seg, cerrado in cortar(ring, junc):
            clave = (tuple(seg), cerrado)
            inverso = (tuple(reversed(seg)), cerrado)
            hecho = cache.get(clave)
            if hecho is not None:
                piezas.append((clave, hecho, False))
                continue
            hecho = cache.get(inverso)
            if hecho is not None:
                piezas.append((inverso, hecho, True))
                continue
            simple = simplificar_arco(seg, cerrado,
                                      _tolerancia(seg, tol_max, tol_piso, fraccion))
            cache[clave] = simple
            piezas.append((clave, simple, False))

        puntos = []
        for clave, simple, invertido in piezas:
            usos[i].append(clave)
            trozo = list(reversed(simple)) if invertido else simple
            if puntos and trozo and puntos[-1] == trozo[0]:
                trozo = trozo[1:]
            puntos.extend(trozo)
        while len(puntos) > 1 and puntos[0] == puntos[-1]:
            puntos.pop()
        if len(puntos) >= 3:
            salida[i] = [(x / q, y / q) for x, y in puntos]

    # cache: clave del arco -> polilinea simplificada, en grados
    arcos = dict((k, [(x / q, y / q) for x, y in v]) for k, v in cache.items())
    return salida, usos, arcos
