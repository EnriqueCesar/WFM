# WFM Intelligence v1.0
## Executive Command Center · Planning is Key

Proyecto PWA listo para GitHub Pages, optimizado y simplificado para usar únicamente las columnas con instrucción.

## Qué incluye

- Executive Score / WFM Score.
- Centro de decisiones: máximo 4 alertas accionables.
- Filtros dinámicos: Región, DM, Tienda, Mes y selección múltiple de semanas.
- Menú limpio: Inicio, Indicadores, Código Pago, NC, Plantilla, Items, Tendencias, Reportes y Configuración.
- Tablas inteligentes con Valor, %, Semana anterior, Variación, Semáforo y Estado.
- Gráficas con eje horizontal, eje vertical y valores visibles.
- Código Pago normalizado.
- NC normalizado.
- Modelo limpio: omite columnas sin instrucción.
- PWA instalable y compatible con GitHub Pages.

## Publicar en GitHub Pages

1. Sube todo el contenido del ZIP al repositorio `wfm_intelligence`.
2. En GitHub ve a **Settings > Pages**.
3. Selecciona **Deploy from branch**.
4. Branch: `main` / folder: `/root`.
5. Guarda y abre el enlace publicado.

## Actualización mensual

La app usa `data/model.json` para cargar rápido. Para actualizar datos:

1. Reemplaza el archivo `data/base.xlsx` con la nueva base mensual.
2. Ejecuta:

```bash
python scripts/refresh_data.py
```

3. Sube el nuevo `data/model.json` a GitHub.

## Columnas usadas

Solo las columnas con instrucción del archivo original:

- Filtros: CC Nombre, DM, Fecha mes, Reg Nom Actual, Semana.
- Indicadores: IPLH, TPLH, Ratio, % NC, Avg Horas Planificadas, Plantilla, Exactitud Kronos, Items, Items SM, Items Kronos, Items Reales, Órdenes Reales.
- Código Pago: solo las columnas `Avg (NC ...)` indicadas.
- NC: solo las columnas `NC ...` indicadas.

## Archivos principales

```text
index.html
manifest.json
sw.js
src/app.js
src/styles.css
data/model.json
scripts/refresh_data.py
assets/logo.png
```
