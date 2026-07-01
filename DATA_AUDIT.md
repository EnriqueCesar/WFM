# WFM Intelligence · Auditoría Fase 1

Base procesada: `Dashboard_WFM(4).xlsx`

- Filas útiles: 24,188
- Columnas detectadas: 142
- Código de Pago normalizado: 11 columnas / 119,679 movimientos no cero
- NC normalizado: 24 columnas / 202,708 movimientos no cero
- Regiones: 11
- DMs: 77
- Tiendas: 953

## Código de Pago
- Act.Promo ← Avg (NC Act. Promo)
- Estandares ← Avg (NC Adm-Estandares de Operacion)
- Hacer Pedido ← Avg (NC Adm-Hacer Pedidos)
- Horarios ← Avg (NC Adm-Horarios)
- Juntas ← Avg (NC Adm-Juntas)
- Reclutamiento ← Avg (NC Adm-Reclutamiento y Selección)
- Admon & Efectivo ← Avg (NC Admon. & Efectivo)
- Admon de Inventarios ← Avg (NC Admon. de Inventarios)
- Capacitacion ← Avg (NC Capacitación)
- Conexiones Partner ← Avg (NC Conexiones Partner)
- RH ← Avg (NC Procesos RH)

## NC
- Break ← Horas Descanso
- Act. Promo ← NC Act. Promo
- Adm-Estandares de Operacion ← NC Adm-Estandares de Operacion
- Adm-Hacer Pedidos ← NC Adm-Hacer Pedidos
- Adm-Horarios ← NC Adm-Horarios
- Adm-Juntas ← NC Adm-Juntas
- Adm-Reclutamiento y Selección ← NC Adm-Reclutamiento y Selección
- Admon. & Efectivo ← NC Admon. & Efectivo
- Admon. de Inventarios ← NC Admon. de Inventarios
- Falta ← NC Ausencia injustificada
- Break ← NC Break
- Capacitación ← NC Capacitación
- Conexiones Partner ← NC Conexiones Partner
- Cumpleaños ← NC Cumpleaños
- Desarrollo y talento ← NC Desarrollo y talento
- Dia Adicional ← NC Dia Adicional
- Gral. Inicial ← NC Incap. Enf. Gral. Inicial
- Gral. Subsecuente ← NC Incap. Enf. Gral. Subsecuente
- Incap. Maternidad ← NC Incap. Maternidad
- Incap. Riesgo de trabajo ← NC Incap. Riesgo de trabajo
- Permiso con Goce ← NC Permiso con Goce
- Permiso sin Goce ← NC Permiso sin Goce
- Procesos RH ← NC Procesos RH
- Vacaciones ← NC Vacaciones

## Entrega
La Fase 1 contiene PWA funcional, modelo normalizado, filtros sincronizados, dashboard ejecutivo, tendencias, Código Pago, NC, Items, Productividad y exportación PDF/impresión.


# FASE 2 · Auditoría Intelligence

## Modelo analítico aplicado

Se mantienen dos familias normalizadas en `data/model.json`:

- `p`: matriz compacta de Código de Pago `[registro, tipo, valor]`.
- `nc`: matriz compacta de NC `[registro, tipo, valor]`.
- `pt`: catálogo de conceptos de Código de Pago.
- `nt`: catálogo de conceptos NC.

Esto evita depender de columnas anchas del Excel y permite calcular porcentajes siempre dentro del filtro activo.

## Validaciones funcionales

- Pareto calcula el total sobre el subconjunto filtrado.
- Heatmap cruza concepto vs semana con intensidad relativa al filtro actual.
- Treemap permite bajar de DM a Tienda y después a concepto.
- Sunburst resume DM, Tienda y Concepto en anillos jerárquicos.
- Comparador semanal calcula Semana A vs Semana B sin modificar la base.

## Nota de mantenimiento

Para nuevas bases, conservar encabezados equivalentes a `Codigo de Pago_*`, `NC_*`, `Items_*`, `Horas_*`, `IPLH`, `TPLH`, `Ratio`, `Exactitud Kronos`, `DM`, `CC Nombre`, `Reg Nom Actual`, `Semana`, `Fecha mes`.
