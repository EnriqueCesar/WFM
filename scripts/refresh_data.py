from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import json, re, math, unicodedata, argparse

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'model.json'
NS='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
REL='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
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
        if isinstance(x,float) and math.isnan(x): return 0.0
        return float(x)
    s=str(x).strip().replace('$','').replace(',','').replace(' ','')
    if s in ('','-','–','—','nan','None'): return 0.0
    is_pct='%' in s; s=s.replace('%','')
    try:
        v=float(s); return v/100 if is_pct and v>1 else v
    except ValueError: return 0.0

def norm_month(s):
    s=clean_text(s).lower()
    ss=''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')
    for m in month_order:
        mm=''.join(c for c in unicodedata.normalize('NFD',m.lower()) if unicodedata.category(c)!='Mn')
        if mm in ss: return m
    return clean_text(s).title()

def colnum(ref):
    m=re.match(r'([A-Z]+)',ref); n=0
    for c in m.group(1): n=n*26+ord(c)-64
    return n-1

def xlsx_rows(path, sheet_name):
    with ZipFile(path) as z:
        shared=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            root=ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in root.iter(NS+'si'):
                shared.append(''.join((t.text or '') for t in si.iter(NS+'t')))
        wb=ET.fromstring(z.read('xl/workbook.xml'))
        rels=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        rmap={r.attrib['Id']:r.attrib['Target'] for r in rels}
        target=None
        for s in wb.find(NS+'sheets'):
            if s.attrib.get('name')==sheet_name:
                target=rmap[s.attrib[REL+'id']]; break
        if not target: raise SystemExit(f'No existe la hoja {sheet_name}')
        sheet_path='xl/'+target.lstrip('/')
        for _,elem in ET.iterparse(z.open(sheet_path),events=('end',)):
            if elem.tag!=NS+'row': continue
            vals={}
            for c in elem.findall(NS+'c'):
                idx=colnum(c.attrib.get('r','A1')); typ=c.attrib.get('t'); v=c.find(NS+'v')
                if typ=='inlineStr':
                    node=c.find(NS+'is'); val=''.join((t.text or '') for t in node.iter(NS+'t')) if node is not None else ''
                elif v is None: val=''
                elif typ=='s': val=shared[int(v.text)]
                elif typ=='b': val=v.text=='1'
                else:
                    txt=v.text or ''
                    try: val=float(txt) if ('.' in txt or 'E' in txt.upper()) else int(txt)
                    except ValueError: val=txt
                vals[idx]=val
            yield [vals.get(i,'') for i in range((max(vals)+1) if vals else 0)]
            elem.clear()

def build(src):
    rows=iter(xlsx_rows(src,'Base_WFM'))
    headers=[clean_text(c) for c in next(rows)]
    idx={h:i for i,h in enumerate(headers)}
    missing=[h for h in list(filters.values())+list(metrics.values())+list(payment_cols.values())+list(nc_cols.values()) if h not in idx]
    if 'NC Break' in missing and 'Horas Descanso' in idx:
        missing.remove('NC Break'); nc_cols['Break']='Horas Descanso'
    D={k:[] for k in ['region','dm','tienda','mes']}; D_index={k:{} for k in D}
    def dim_id(k,v):
        v=norm_month(v) if k=='mes' else clean_text(v)
        if v not in D_index[k]: D_index[k][v]=len(D[k]); D[k].append(v)
        return D_index[k][v]
    R=[]; P=[]; N=[]; seen=set(); duplicates=0
    for row in rows:
        if not row: continue
        def get(h):
            i=idx.get(h,-1); return row[i] if i>=0 and i<len(row) else ''
        semana=parse_num(get(filters['semana']))
        if not semana: continue
        dims=[dim_id('region',get(filters['region'])),dim_id('dm',get(filters['dm'])),dim_id('tienda',get(filters['tienda'])),dim_id('mes',get(filters['mes'])),int(semana)]
        values=[]
        for key,h in metrics.items():
            v=parse_num(get(h))
            if key in ('NC_Pct','Exactitud_Kronos') and v>1.5: v/=100
            values.append(round(v,6))
        signature=tuple(dims+values)
        if signature in seen:
            duplicates+=1; continue
        seen.add(signature); R.append(dims+values); ri=len(R)-1
        for pi,(label,h) in enumerate(payment_cols.items()):
            v=parse_num(get(h))
            if v>0: P.append([ri,pi,round(v,4)])
        for ni,(label,h) in enumerate(nc_cols.items()):
            v=parse_num(get(h))
            if v>0: N.append([ri,ni,round(v,4)])
    weeks=sorted({r[4] for r in R})
    model={'version':'2.0-semana-27-ui-refinement','meta':{'rows':len(R),'source':Path(src).name,'sheet':'Base_WFM','latestWeek':max(weeks) if weeks else None,'weeks':weeks,'duplicatesRemoved':duplicates,'rule':'Lectura por nombre de hoja y encabezado; historial conservado.','missing':missing},'dims':D,'monthOrder':month_order,'metrics':list(metrics.keys()),'metricLabels':{'IPLH':'IPLH','TPLH':'TPLH','Ratio':'Ratio gerencial','NC_Pct':'% NC','Horas_Planificadas':'Horas planificadas','Plantilla_Ideal':'Plantilla ideal','Plantilla_Real':'Plantilla real','Exactitud_Kronos':'Exactitud Kronos','Items_ADT':'Items / ADT','Items_Ajuste_SM':'Items Ajuste SM','Items_Kronos':'Items Kronos','Items_Reales':'Items Reales','Ordenes_Reales':'Órdenes reales'},'rows':R,'paymentTypes':list(payment_cols.keys()),'payments':P,'ncTypes':list(nc_cols.keys()),'nc':N}
    OUT.write_text(json.dumps(model,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print(json.dumps({'rows':len(R),'week27':sum(1 for r in R if r[4]==27),'latestWeek':model['meta']['latestWeek'],'duplicatesRemoved':duplicates,'missing':missing,'output':str(OUT)},ensure_ascii=False))

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('source',nargs='?',default=str(ROOT/'data'/'base.xlsx'))
    args=ap.parse_args(); build(Path(args.source))
