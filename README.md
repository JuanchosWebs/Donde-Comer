# Donde Comer — sitio que se actualiza solo

Esta carpeta es un sitio web completo que podés subir a GitHub para que:

1. Se actualice solo cada vez que reemplaces el Excel (sin pedirme nada a mí).
2. Use Google Maps de verdad en vez del mapa ilustrado / OpenStreetMap.

## Cómo queda armado

- `data/Donde Comer.xlsx` → tu Excel. Es el único archivo que vas a tocar de acá en adelante.
- `data/geocode_cache.json` → memoria de direcciones ya ubicadas en el mapa (no la toques, se actualiza sola).
- `scripts/` → el código Python que lee el Excel y arma la página (lo mismo que vengo corriendo yo, pero automatizado).
- `site/template.html` → el diseño de la página (filtros, tarjetas, mapa).
- `.github/workflows/deploy.yml` → la automatización de GitHub que corre todo esto y publica el resultado.

Cuando subís un Excel nuevo, GitHub solo (sin que yo intervenga) hace: lee el Excel → geocodifica las direcciones nuevas → arma la página → la publica. Tarda entre 1 y 10 minutos según cuántas direcciones nuevas haya.

## Paso 1 — Crear el repositorio

1. Entrá a [github.com/new](https://github.com/new).
2. Nombre del repositorio: el que quieras (por ejemplo `donde-comer`).
3. Dejalo **público** (con la cuenta gratuita de GitHub, un repo privado igual publica la página en una URL pública sin login — así que no suma privacidad real; si te importa, avisame y vemos alternativas).
4. Creá el repositorio vacío (sin README, sin .gitignore — ya te los llevás en esta carpeta).
5. En la página del repo, hacé clic en **"Add file" → "Upload files"**, y arrastrá **todo el contenido** de esta carpeta (incluidas las subcarpetas `data/`, `scripts/`, `site/`, `.github/` — los navegadores modernos como Chrome permiten arrastrar carpetas enteras y GitHub conserva la estructura de subcarpetas). Confirmá el commit ("Primer commit" o lo que quieras).

## Paso 2 — Activar GitHub Pages

1. En el repo, andá a **Settings → Pages**.
2. En "Build and deployment" → "Source", elegí **GitHub Actions** (no "Deploy from a branch").
3. No hace falta nada más acá — el workflow ya incluido se encarga del resto.

## Paso 3 — Conseguir la API key de Google Maps

1. Entrá a [console.cloud.google.com](https://console.cloud.google.com/) con tu cuenta de Google y creá un proyecto nuevo (arriba a la izquierda, "Select a project" → "New Project"). Nombre: el que quieras, por ejemplo "Donde Comer".
2. Con el proyecto seleccionado, andá a **APIs & Services → Library**, buscá **"Maps JavaScript API"** y hacé clic en **Enable**.
3. Andá a **Billing** (facturación) desde el menú y asociá una cuenta de facturación con una tarjeta. Google la pide para habilitar la API aunque no llegues a pagar nada — el uso normal de este sitio (uso personal, no miles de visitas) se mantiene dentro del **tramo gratuito de 10.000 cargas de mapa por mes**; recién después de eso cobra (~USD 7 cada 1.000 cargas adicionales).
4. Andá a **APIs & Services → Credentials → Create Credentials → API key**. Se genera una key (una cadena larga de letras y números). Copiala.
5. Hacé clic en esa key para editarla y, en **"Application restrictions"**, elegí **"Websites"** (HTTP referrers) y agregá:
   - `TU-USUARIO.github.io/*`
   - Si vas a usar un dominio propio más adelante, agregalo también.
   Esto evita que otra persona use tu key desde otro sitio.
6. En **"API restrictions"**, elegí "Restrict key" y marcá solo **Maps JavaScript API**.

## Paso 4 — Cargar la API key en GitHub (sin que quede visible en el código)

1. En el repo, andá a **Settings → Secrets and variables → Actions → New repository secret**.
2. Nombre: `GOOGLE_MAPS_API_KEY`. Valor: pegá la key del paso anterior.
3. Guardá.

## Paso 5 — Disparar la primera publicación

1. Andá a la pestaña **Actions** del repo. Debería aparecer un workflow corriendo llamado "Actualizar y publicar Donde Comer" (se dispara solo al subir los archivos en el Paso 1; si no arrancó, hacé clic en él y en "Run workflow").
2. La primera vez tarda varios minutos porque geocodifica las ~550 direcciones una por una (para no saturar el servicio gratuito que usamos, OpenStreetMap/Nominatim). Las próximas veces es mucho más rápido: solo geocodifica las direcciones nuevas que agregues.
3. Cuando termine (tilde verde), la URL de tu sitio va a ser `https://TU-USUARIO.github.io/NOMBRE-DEL-REPO/` (también la vas a ver en Settings → Pages).

## Cómo actualizar de acá en adelante

1. Entrá al repo en github.com, abrí la carpeta `data`.
2. Hacé clic en `Donde Comer.xlsx` → ícono de lápiz o "..." → **"Upload files"** (o borrá el archivo viejo y subí el nuevo con el mismo nombre exacto: `Donde Comer.xlsx`).
3. Confirmá el commit.
4. Esperá 1 o 2 minutos (podés ver el progreso en la pestaña **Actions**) y refrescá la web — va a tener los lugares nuevos, con Google Maps y todos los filtros funcionando.

Lo que ya marcaste como visitado y las notas que escribiste **no se pierden**, porque se guardan en el navegador de cada persona que entra al sitio (no en el Excel).

## Si aparece un barrio nuevo

El archivo `scripts/coords.py` tiene una coordenada aproximada por barrio, que se usa solo como respaldo cuando una dirección puntual no se puede ubicar automáticamente. Si agregás lugares en un barrio que todavía no está en esa lista, avisame y te paso la línea para agregar (o abrí el archivo y sumala vos mismo: es simplemente `"Nombre del barrio": (latitud, longitud)`, podés sacar la latitud/longitud aproximada buscando el barrio en Google Maps y copiando las coordenadas del centro).

## Costos esperables

- **GitHub Pages y GitHub Actions:** gratis para este uso (muy por debajo de los límites de la cuenta gratuita).
- **Google Maps:** gratis en la práctica — el tramo gratuito (10.000 cargas de mapa por mes) alcanza para muchísimo más tráfico del que va a tener un dashboard personal.
- **Geocodificación (Nominatim/OpenStreetMap):** gratis, sin límite de uso relevante para este caso (solo direcciones nuevas, una vez cada vez que actualizás el Excel).
