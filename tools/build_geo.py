import json, math
from shapely.geometry import shape, MultiPolygon, Polygon, box
from shapely.ops import unary_union, transform, polylabel
from pyproj import Transformer
G='caop_GeoJSON/'   # clonar https://github.com/nmota/caop_GeoJSON para esta pasta
def load(f):
    d=json.load(open(G+f,encoding='utf-8-sig'))
    epsg=d['crs']['properties']['name'].split(':')[-1]
    tr=Transformer.from_crs('EPSG:'+epsg,'EPSG:4326',always_xy=True)
    out=[]
    for ft in d['features']:
        g=shape(ft['geometry']).buffer(0)
        g=transform(lambda x,y,z=None: tr.transform(x,y), g)
        out.append((ft['properties'],g))
    return out
LOW={'de','do','da','dos','das','e','a'}
def tc(s):
    w=s.lower().split()
    return ' '.join(x if (i>0 and x in LOW) else x[:1].upper()+x[1:] for i,x in enumerate(w)).replace('Vila Real de Santo António','Vila Real de Santo António')
def parts(g): return list(getattr(g,'geoms',[g]))
def clean(g,minarea):
    ps=[p for p in parts(g) if p.area>=minarea]
    return MultiPolygon(ps) if len(ps)>1 else (ps[0] if ps else g)
class View:
    def __init__(s,geoms,W,maxH=None,pad=4):
        U=unary_union(geoms); minx,miny,maxx,maxy=U.bounds
        s.k=math.cos(math.radians((miny+maxy)/2))
        sw=(maxx-minx)*s.k; sh=(maxy-miny)
        s.sc=(W-2*pad)/sw
        if maxH and sh*s.sc>maxH-2*pad: s.sc=(maxH-2*pad)/sh
        s.minx,s.maxy,s.pad=minx,maxy,pad
        s.W=round(sw*s.sc+2*pad); s.H=round(sh*s.sc+2*pad)
    def px(s,g,ox=0,oy=0):
        return transform(lambda x,y,z=None:((x-s.minx)*s.k*s.sc+s.pad+ox,(s.maxy-y)*s.sc+s.pad+oy),g)
def path(g,tol=0.7):
    g=g.simplify(tol,preserve_topology=True); dd=''
    for p in parts(g):
        if p.is_empty or p.area<0.6: continue
        pts=list(p.exterior.coords)[:-1]
        dd+='M'+' '.join(f'{round(a)},{round(b)}' for a,b in pts)+'Z'
    return dd
def lab(g):
    big=max(parts(g),key=lambda p:p.area)
    try: c=polylabel(big,0.5)
    except Exception: c=big.representative_point()
    return round(c.x),round(c.y)
def slug(s):
    import unicodedata,re
    return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode()).strip('-')

dist=load('ContinenteDistritos.geojson')
conc=load('ContinenteConcelhos.geojson')
mad=load('Madeira/MadeiraConcelhos.geojson')
mad=[(p,clean(g.intersection(box(-17.5,32.3,-16.0,33.2)),1e-5)) for p,g in mad]   # sem Selvagens
mad=[(p,g) for p,g in mad if not g.is_empty]
from shapely import affinity
def madfix(p,g):
    if p['Municipio']=='Porto Santo': return affinity.translate(g,-0.12,-0.16)
    if p['Municipio']=='Santa Cruz': return clean(g.intersection(box(-17.5,32.62,-16.0,33.2)),1e-5)
    return g
mad=[(p,madfix(p,g)) for p,g in mad]
aco=[]
from shapely import affinity as _af
for f,dx,dy in [('AçoresOcidentalConcelhos',2.3,-0.35),('AçoresCentralConcelhos',0,0),('AçoresOrientalConcelhos',-0.9,0.45)]:
    aco+=[(p,_af.translate(g,dx,dy)) for p,g in load('Açores/'+f+'.geojson')]
aco=[(p,clean(g,1e-6)) for p,g in aco]

out={'pt':{},'sub':{}}
# --- vista Portugal: continente à direita, ilhas em caixas à esquerda
W,H=440,560
cv=View([g for _,g in dist],W=270,maxH=H-10)
ox=W-cv.W-2; oy=(H-cv.H)//2
items=[]
for p,g in dist:
    gp=cv.px(g,ox,oy); n=tc(p['Distrito']); lx,ly=lab(gp)
    items.append({'id':slug(n),'n':n,'d':path(gp,1.0),'lx':lx,'ly':ly})
def inset(geoms,x,y,w,h,tol):
    v=View(geoms,W=w,maxH=h,pad=6); dx=x+(w-v.W)/2; dy=y+(h-v.H)/2
    return ''.join(path(v.px(g,dx,dy),tol) for g in geoms)
BW,BH=150,105
out['pt']={'W':W,'H':H,'items':items,'ins':[
  {'id':'acores','n':'Açores','x':6,'y':150,'w':BW,'h':BH,'d':inset([g for _,g in aco],6,150,BW,BH,0.3)},
  {'id':'madeira','n':'Madeira','x':6,'y':290,'w':BW,'h':BH,'d':inset([g for _,g in mad],6,290,BW,BH,0.3)}]}
# --- vistas de concelhos
def subview(key,name,lst,W=420,maxH=520,tol=1.3):
    v=View([g for _,g in lst],W=W,maxH=maxH)
    its=[]
    for n,g in lst:
        gp=v.px(g); lx,ly=lab(gp)
        a=gp.area
        its.append({'n':n,'id':slug(n),'d':path(gp,tol),'lx':lx,'ly':ly,'fs':(10 if a>4000 else 9 if a>1800 else 8 if a>700 else 0)})
    out['sub'][key]={'n':name,'W':v.W,'H':v.H,'items':its}
for p,g in dist:
    n=tc(p['Distrito'])
    lst=[(tc(cp['Concelho']),cg) for cp,cg in conc if cp['Distrito']==p['Distrito']]
    subview(slug(n),'Distrito de '+n,lst)
subview('madeira','Região Autónoma da Madeira',[(p['Municipio'],g) for p,g in mad],tol=0.9)
subview('acores','Região Autónoma dos Açores',[(tc(p['MUNICIPIO']),g) for p,g in aco],tol=0.6,maxH=320)
s=json.dumps(out,ensure_ascii=False,separators=(',',':'))
open('geo.json','w').write(s); print(len(s))
for k,v in out['sub'].items(): print(k,v['W'],v['H'],len(v['items']))
