"""Combina site/template.html con los datos generados por build.py y produce
dist/index.html, listo para publicar en GitHub Pages.
"""
import datetime
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD_DIR = os.path.join(ROOT, "build")
SITE_DIR = os.path.join(ROOT, "site")
DIST_DIR = os.path.join(ROOT, "dist")

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def js_json(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def load(name):
    with open(os.path.join(BUILD_DIR, f"{name}.json"), encoding="utf-8") as f:
        return json.load(f)


def assemble():
    places = load("places")
    cats = load("cats")
    subcats = load("subcats")
    barrios = load("barrios")
    localidades = load("localidades")

    with open(os.path.join(SITE_DIR, "template.html"), encoding="utf-8") as f:
        tpl = f.read()

    api_key = os.environ.get("GOOGLE_MAPS_API_KEY", "")
    today = datetime.date.today()
    updated = f"{today.day} de {MESES[today.month - 1]} de {today.year}"

    out = tpl
    out = out.replace("__PLACES_JSON__", js_json(places))
    out = out.replace("__CATS_JSON__", js_json(cats))
    out = out.replace("__SUBCATS_JSON__", js_json(subcats))
    out = out.replace("__BARRIOS_JSON__", js_json(barrios))
    out = out.replace("__LOCALIDADES_JSON__", js_json(localidades))
    out = out.replace("__PLACE_COUNT__", str(len(places)))
    out = out.replace("__UPDATED_DATE__", updated)
    out = out.replace("__GOOGLE_MAPS_API_KEY__", api_key)

    os.makedirs(DIST_DIR, exist_ok=True)
    out_path = os.path.join(DIST_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)

    print(f"wrote {len(out)} bytes to {out_path}")


if __name__ == "__main__":
    assemble()
