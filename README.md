# ☕ WFM Intelligence
## Planning is Key
**Workforce Management Executive Suite**

Proyecto PWA listo para GitHub Pages.

## Entrega Fase 1
- PWA instalable y offline.
- Diseño ejecutivo estilo Starbucks.
- Filtros sincronizados: Región, DM, Tienda, Mes, Semana, Formato y Categoría.
- Dashboard Ejecutivo con 8 KPIs inteligentes.
- Módulos: Executive, Productividad, Plantilla, Horas, Código Pago, NC, Items, Tendencias, Forecast, Mapa y Reportes.
- Normalización automática ya aplicada a familias `Codigo de Pago_*` y `NC_*`.
- Exportación PDF por impresión en formato limpio.
- Modelo optimizado en `/data/model.json` para no subir el Excel pesado al repositorio.

## Publicar en GitHub Pages
1. Crea el repositorio `wfm_intelligence`.
2. Sube todo el contenido de esta carpeta.
3. En GitHub: Settings → Pages → Deploy from branch → `main` → `/root`.
4. Abre la URL publicada.

## Actualización mensual
La Fase 1 incluye el modelo ya convertido. Para actualizar con otra base, reemplaza el Excel en local y ejecuta el script de conversión incluido en `scripts/refresh_data.py`.

## Nota de peso
El Excel original supera 20 MB. Para mantener el proyecto optimizado, el ZIP no incluye el `.xlsx`; incluye el modelo web comprimible y listo para uso.
