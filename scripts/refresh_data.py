from openpyxl import load_workbook
from pathlib import Path
import json, re, math, unicodedata
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data'/'base.xlsx'
OUT=ROOT/'data'/'model.json'
filters={'tienda':'CC Nombre','dm':'DM','mes':'Fecha mes','region':'Reg Nom Actual','semana':'Semana'}
metrics={'IPLH':'IPLH','TPLH':'TPLH','Ratio':'Ratio','NC_Pct':'% NC','Horas_Planificadas':'Avg (Horas Planificadas)','Plantilla_Ideal':'Emp. Autorizados','Plantilla_Real':'Emp. Reales','Exactitud_Kronos':'Exactitud Kronos','Items_ADT':'Items','Items_Ajuste_SM':'Items Gerente (Aj.)','Items_Kronos':'Items Kronos (Proy.)','Items_Reales':'Items Reales','Ordenes_Reales':'Ordenes Reales'}
payment_cols={'Act. Promo':'Avg (NC Act. Promo)','Estándares':'Avg (NC Adm-Estandares de Operacion)','Hacer Pedido':'Avg (NC Adm-Hacer Pedidos)','Horarios':'Avg (NC Adm-Horarios)','Juntas':'Avg (NC Adm-Juntas)','Reclutamiento':'Avg (NC Adm-Reclutamiento y Selección)','Admon & Efectivo':'Avg (NC Admon. & Efectivo)','Admon de Inventarios':'Avg (NC Admon. de Inventarios)','Capacitación':'Avg (NC Capacitación)','Conexiones Partner':'Avg (NC Conexiones Partner)','RH':'Avg (NC Procesos RH)'}
nc_cols={'Falta':'NC Ausencia injustificada','Break':'NC Break','Cumpleaños':'NC Cumpleaños','Día Adicional':'NC Dia Adicional','Gral. Inicial':'NC Incap. Enf. Gral. Inicial','Gral. Subsecuente':'NC Incap. Enf. Gral. Subsecuente','Incap. Maternidad':'NC Incap. Maternidad','Riesgo de trabajo':'NC Incap. Riesgo de trabajo','Permiso con Goce':'NC Permiso con Goce','Permiso sin Goce':'NC Permiso sin Goce'}
month_order=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
def clean_text(x):
    if x is None: return ''
    return re.sub(r'\s+',' ',str(x).strip())
def parse_num(x):
    if x is None: return 0.0
    if isinstance(x,(int,float)):
        if math.isnan(float(x)): return 0.0
        return float(x)
    s=str(x).strip().replace('$','').replace(',','').replace(' ','')
    if s in ('','-','–','—','nan','None'): return 0.0
    is_pct='%' in s
    s=s.replace('%','')
    try:
        v=float(s)
        return v/100 if is_pct and v>1 else v
    except Exception:
        return 0.0
def norm_month(s):
    s=clean_text(s).lower()
    ss=''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')
    for m in month_order:
        mm=''.join(c for c in unicodedata.normalize('NFD',m.lower()) if unicodedata.category(c)!='Mn')
        if mm in ss: return m
    return clean_text(s).title()
if not SRC.exists():
    raise SystemExit('No existe data/base.xlsx. Coloca la base mensual con ese nombre.')
wb=load_workbook(SRC,read_only=True,data_only=True)
ws=wb['Base_WFM']
headers=[clean_text(c) for c in next(ws.iter_rows(min_row=1,max_row=1,values_only=True))]
idx={h:i for i,h in enumerate(headers)}
missing=[h for h in list(filters.values())+list(metrics.values())+list(payment_cols.values())+list(nc_cols.values()) if h not in idx]
if 'NC Break' in missing and 'Horas Descanso' in idx:
    missing.remove('NC Break'); nc_cols['Break']='Horas Descanso'
D={k:[] for k in ['region','dm','tienda','mes']}; D_index={k:{} for k in D}
def dim_id(k,v):
    v=norm_month(v) if k=='mes' else clean_text(v)
    if v not in D_index[k]: D_index[k][v]=len(D[k]); D[k].append(v)
    return D_index[k][v]
R=[]; P=[]; N=[]
for row in ws.iter_rows(min_row=2,values_only=True):
    if not any(row): continue
    semana=parse_num(row[idx[filters['semana']]])
    if not semana: continue
    r=[dim_id('region',row[idx[filters['region']]]),dim_id('dm',row[idx[filters['dm']]]),dim_id('tienda',row[idx[filters['tienda']]]),dim_id('mes',row[idx[filters['mes']]]),int(semana)]
    for key,h in metrics.items():
        v=parse_num(row[idx[h]]) if h in idx else 0
        if key in ['NC_Pct','Exactitud_Kronos'] and v>1.5: v/=100
        r.append(round(v,6))
    R.append(r); ri=len(R)-1
    for pi,(label,h) in enumerate(payment_cols.items()):
        v=parse_num(row[idx[h]]) if h in idx else 0
        if v>0: P.append([ri,pi,round(v,4)])
    for ni,(label,h) in enumerate(nc_cols.items()):
        v=parse_num(row[idx[h]]) if h in idx else 0
        if v>0: N.append([ri,ni,round(v,4)])
model={'version':'1.0-clean','meta':{'rows':len(R),'source':'data/base.xlsx','rule':'Solo columnas con instrucción. Columnas sin instrucción omitidas.','missing':missing},'dims':D,'monthOrder':month_order,'metrics':list(metrics.keys()),'metricLabels':{'IPLH':'IPLH','TPLH':'TPLH','Ratio':'Ratio gerencial','NC_Pct':'% NC','Horas_Planificadas':'Horas planificadas','Plantilla_Ideal':'Plantilla ideal','Plantilla_Real':'Plantilla real','Exactitud_Kronos':'Exactitud Kronos','Items_ADT':'Items / ADT','Items_Ajuste_SM':'Items Ajuste SM','Items_Kronos':'Items Kronos','Items_Reales':'Items Reales','Ordenes_Reales':'Órdenes reales'},'rows':R,'paymentTypes':list(payment_cols.keys()),'payments':P,'ncTypes':list(nc_cols.keys()),'nc':N}
OUT.write_text(json.dumps(model,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(f'Modelo actualizado: {len(R):,} registros · {OUT}')
