import json
from shapely.geometry import shape, MultiPolygon, Polygon, box
from shapely.ops import unary_union
d=json.load(open('caop_GeoJSON/Madeira/MadeiraFreguesias.geojson'))
fs=[f for f in d['features'] if f['properties'].get('Municipio')=='Funchal']
geoms={}
for f in fs:
    n=f['properties']['Freguesia'].replace('Funchal (','').replace(')','')
    g=shape(f['geometry'])
    geoms[n]=g
allu=unary_union(list(geoms.values()))
# keep main island: polygons within big bbox around the largest component's area
main=max((p for g in geoms.values() for p in getattr(g,'geoms',[g])), key=lambda p:p.area)
cx,cy=main.centroid.x, main.centroid.y
clip=box(cx-20000,cy-20000,cx+20000,cy+20000)
for n in geoms:
    g=geoms[n].intersection(clip)
    parts=[p for p in getattr(g,'geoms',[g]) if p.area>2000]   # drop rocks/islets < 0.2 ha
    geoms[n]=MultiPolygon(parts) if len(parts)>1 else parts[0]
U=unary_union(list(geoms.values()))
minx,miny,maxx,maxy=U.bounds
W=380; s=W/(maxx-minx); H=round((maxy-miny)*s)
print('extent km',(maxx-minx)/1000,(maxy-miny)/1000,'H',H)
def P(x,y): return (round((x-minx)*s,1), round((maxy-y)*s,1))
SHORT={"Santo António":"Santo António","São Roque":"S. Roque","Monte":"Monte","São Gonçalo":"S. Gonçalo","Santa Maria Maior":"Sta M. Maior","Santa Luzia":"Sta Luzia","Imaculado Coração de Maria":"I.C. Maria","São Pedro":"S. Pedro","Sé":"Sé","São Martinho":"S. Martinho"}
out=[]
for n,g in geoms.items():
    g=g.simplify(18, preserve_topology=True)
    dd=''
    for p in getattr(g,'geoms',[g]):
        pts=[P(x,y) for x,y in p.exterior.coords]
        dd+='M'+' '.join(f'{a},{b}' for a,b in pts[:-1])+'Z'
    rp=geoms[n].representative_point(); lx,ly=P(rp.x,rp.y)
    area=geoms[n].area/1e4
    fs_=10 if area>600 else (9 if area>300 else 8)
    out.append({'name':n,'short':SHORT[n],'lx':lx,'ly':ly,'fs':fs_,'d':dd})
    print(n, len(dd), round(area))
json.dump({'H':H,'map':out},open('map.json','w'),ensure_ascii=False)
