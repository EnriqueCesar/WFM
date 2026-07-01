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


## Entrega Fase 2 · Intelligence

Incluye actualización completa para análisis dinámico:

- Código de Pago Intelligence con modelo normalizado.
- NC Intelligence con modelo normalizado.
- Heatmap Código de Pago por semana.
- Heatmap NC por semana.
- Pareto interactivo 80/20.
- Treemap con drill down Región → DM → Tienda → Concepto.
- Sunburst jerárquico para lectura ejecutiva.
- Insights automáticos por filtro activo.
- Comparador semanal A vs B.
- Optimización para mantener el proyecto por debajo de 20 MB sin incluir el Excel original.

### Uso operativo

1. Entra a **Código Pago** o **NC**.
2. Ajusta filtros de Región, DM, Tienda, Mes, Semana, Formato o Categoría.
3. Revisa Pareto para priorizar.
4. Usa Heatmap para detectar semanas con concentración.
5. Usa Treemap/Sunburst para entender dónde está el impacto.
6. Usa Comparador semanal para validar crecimiento o reducción.


## FASE 3

Esta versión agrega Forecast Intelligence, Items Intelligence, Insights automáticos, Comparador ejecutivo y Exportación PDF profesional.

Para generar PDF: abre la página `Reportes` y presiona el botón `PDF`. Selecciona guardar como PDF en el navegador.
