"""Exact bounded search, not a proof of global nonexistence.

For anchors a,b with ab+1 square, enumerate reduced m/n, |m|<=H,
1<=n<=H and x=4mn(m-n)(bn-am)/(am^2-bn^2)^2. Save all
vertices and all edges; enumerate triangles/K4 in the resulting graph.
"""
from fractions import Fraction as Q
from math import gcd,isqrt
from itertools import combinations
from pathlib import Path
import argparse,json,time,hashlib,concurrent.futures
from core import square_certificate,sqrtq

def search_one(task):
 a,b,H,outdir=task;t0=time.monotonic();pool={};parameters=0
 assert a and b and a!=b and sqrtq(a*b+1) is not None
 for n in range(1,H+1):
  for m in range(-H,H+1):
   if gcd(m,n)!=1:continue
   parameters+=1;D=a*m*m-b*n*n;N=4*m*n*(m-n)*(b*n-a*m)
   if not D or not N:continue
   x=Q(N,D*D)
   if x in (a,b):continue
   if x not in pool or abs(D)<pool[x][1]:pool[x]=(N,abs(D),m,n)
 xs=sorted(pool);raw=[pool[x] for x in xs];d2=[z[1]**2 for z in raw];nums=[z[0] for z in raw]
 forward=[set() for _ in xs];edges=[];tested=0
 for i in range(len(xs)):
  Ni=nums[i];Di=d2[i]
  for j in range(i+1,len(xs)):
   tested+=1;s=Ni*nums[j]+Di*d2[j]
   if s<0:continue
   r=isqrt(s)
   if r*r==s:
    edges.append([i,j]);forward[i].add(j)
 triangles=[];k4=[]
 for i,j in edges:
  for k in sorted(forward[i]&forward[j]):
   triangles.append([i,j,k])
   for l in sorted(forward[i]&forward[j]&forward[k]):k4.append([i,j,k,l])
 witnesses=[square_certificate([a,b]+[xs[i] for i in ids]) for ids in k4]
 for w in witnesses:assert w['distinct'] and w['nonzero'] and all(e['root'] is not None for e in w['pairs'])
 doc={'schema':'anchor-graph-v1','anchors':[a,b],'parameter_height':H,'parameter_domain':'gcd(m,n)=1, -H<=m<=H, 1<=n<=H','parameters_enumerated':parameters,'vertices':[{'x':str(x),'m':raw[i][2],'n':raw[i][3]} for i,x in enumerate(xs)],'edges':edges,'triangles':triangles,'K4':k4,'sextuple_certificates':witnesses,'pair_tests':tested,'arithmetic':'Python arbitrary-precision integers and math.isqrt; no floating point','conclusion_scope':'only the listed finite parameter box','elapsed_seconds':round(time.monotonic()-t0,6)}
 name=f'anchor_{a}_{b}_H{H}.json';p=Path(outdir)/name;p.write_text(json.dumps(doc,separators=(',',':'))+'\n')
 return {'file':name,'anchors':[a,b],'H':H,'parameters':parameters,'vertices':len(xs),'edges':len(edges),'triangles':len(triangles),'K4':len(k4),'pair_tests':tested,'elapsed_seconds':doc['elapsed_seconds'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--height',type=int,default=40);ap.add_argument('--anchor-max',type=int,default=40);ap.add_argument('--workers',type=int,default=4);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--selected',action='store_true');args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
 pairs=[(a,b) for a in range(1,args.anchor_max+1) for b in range(a+1,args.anchor_max+1) if isqrt(a*b+1)**2==a*b+1]
 if args.selected:pairs=[(1,3),(1,8),(3,8),(1,120),(3,120),(8,120),(-1,1)]
 else:pairs+= [p for p in [(1,120),(3,120),(8,120),(-1,1)] if p not in pairs]
 tasks=[(a,b,args.height,str(args.output)) for a,b in pairs];rows=[]
 with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
  for row in pool.map(search_one,tasks):rows.append(row);print(json.dumps(row),flush=True)
 (args.output/'summary.json').write_text(json.dumps({'scope':'finite search only','rows':rows,'total_pair_tests':sum(r['pair_tests'] for r in rows),'total_K4':sum(r['K4'] for r in rows)},indent=2)+'\n')
