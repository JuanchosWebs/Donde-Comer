"""Geocodifica direcciones usando Nominatim (OpenStreetMap), gratis y sin API key.

Guarda cada resultado en un archivo cache (data/geocode_cache.json) para no volver
a pedir la misma dirección dos veces: solo se geocodifican las direcciones nuevas
en cada build. Respeta la política de uso de Nominatim (máximo 1 pedido por segundo,
identificando la app con un User-Agent).
"""
import json
import time
import urllib.parse
import urllib.request

# Nominatim pide identificar la aplicación. Si el uso crece, es buena práctica
# sumar un email de contacto acá (ver https://operations.osmfoundation.org/policies/nominatim/).
USER_AGENT = "DondeComerBA-static-site/1.0 (uso personal)"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def _fetch(query):
    url = NOMINATIM_URL + "?" + urllib.parse.urlencode({
        "format": "json",
        "limit": 1,
        "countrycodes": "ar",
        "q": query,
    })
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    return None


def geocode_places(places, cache_path):
    """Rellena p['lat']/p['lon']/p['approx'] in-place para cada lugar con 'geo'.

    Los lugares sin 'geo' (o los que no se pueden geocodificar) se quedan con
    las coordenadas de fallback (centro del barrio) que ya trae build.py.
    """
    try:
        with open(cache_path, encoding="utf-8") as f:
            cache = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        cache = {}

    changed = False
    new_lookups = 0
    for p in places:
        geo = p.get("geo")
        if not geo:
            continue
        if geo in cache:
            lat, lon = cache[geo]
            p["lat"], p["lon"], p["approx"] = lat, lon, False
            continue
        try:
            result = _fetch(geo)
        except Exception:
            result = None
        new_lookups += 1
        if result:
            cache[geo] = list(result)
            p["lat"], p["lon"], p["approx"] = result[0], result[1], False
            changed = True
        # 1 pedido por segundo como máximo, sin importar si hubo error o no
        time.sleep(1.1)

    if changed:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=0, sort_keys=True)

    print(f"geocode: {new_lookups} direcciones nuevas geocodificadas, {len(cache)} en cache")
