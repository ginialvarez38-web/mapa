#!/usr/bin/env python3
"""Inyecta data/world.json en la plantilla y escribe index.html.

El resultado es un unico archivo sin dependencias externas: se abre con doble
clic desde el disco y funciona igual servido por HTTP.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TPL = os.path.join(ROOT, "src", "globo.template.html")
DATA = os.path.join(ROOT, "data", "world.json")
OUT = os.path.join(ROOT, "index.html")


def main():
    with open(TPL, "r", encoding="utf-8") as fh:
        tpl = fh.read()
    with open(DATA, "r", encoding="utf-8") as fh:
        data = fh.read()

    if "__WORLD_DATA__" not in tpl:
        print("la plantilla no tiene el marcador __WORLD_DATA__", file=sys.stderr)
        return 1

    json.loads(data)  # falla pronto si el blob esta corrupto

    # Un "</script>" dentro del JSON cerraria la etiqueta antes de tiempo.
    data = data.replace("</", "<\\/")

    html = tpl.replace("__WORLD_DATA__", data)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)

    print("index.html: %.1f KB" % (os.path.getsize(OUT) / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
