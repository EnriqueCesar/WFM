# WFM Intelligence

## v2-semana-27-ui-refinement

Dashboard operativo WFM actualizado con información histórica y datos disponibles hasta la **Semana 27**.

### Fuente

- Archivo fuente: `Dashboard_WFM.xlsx`
- Hoja utilizada: `Base_WFM`
- Lectura por nombre de hoja y encabezado, sin depender de posiciones fijas de columnas.
- Data publicada en `data/model.json`.

### Cambios

- Integración de Semana 27 sin eliminar información histórica.
- Menú **Configuración** oculto; su lógica de procesamiento permanece en el proyecto.
- Navegación operativa simplificada.
- Iconografía SVG monoline consistente.
- Interfaz refinada con tarjetas modulares, jerarquía visual, tablas legibles y vista responsive.
- Paleta corporativa basada en verde `#006241`.
- Mejoras de impresión y exportación a PDF.

### Validaciones ejecutadas

- Generación del modelo desde `Base_WFM`.
- Semana más reciente: 27.
- Registros Semana 27: 942.
- Duplicados exactos eliminados: 0.
- Encabezados requeridos faltantes: 0.
- Validación de sintaxis JavaScript.
- Validación de `manifest.json` y rutas estáticas.
- Compatibilidad con GitHub Pages y PWA conservada.
- Ningún archivo del proyecto supera 20 MB.

### Actualización de data

```bash
python scripts/refresh_data.py /ruta/Dashboard_WFM.xlsx
```

### Despliegue

Publicar la raíz del repositorio mediante GitHub Pages. Todas las rutas son relativas y no requieren servidor de aplicación.
