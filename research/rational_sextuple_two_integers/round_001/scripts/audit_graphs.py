"""Second exact implementation: regenerates vertices and every edge, then DFS.
No code is imported from the primary search. This is a computational cross-check,
not an independent model review and not a formal proof assistant certificate.
"""
from fractions import Fraction
from math import gcd,isqrt
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import argparse,hashlib,json,time

RES64=frozenset(i*i%64 for i in range(64))
RES63=frozenset(i*i%63 for i in range(63))

def audit(path_string):
 start=time.monotonic();path=Path(path_string);obj=json.loads(path.read_text())
 a,b=obj['anchors'];H=obj['parameter_height'];found=set();parameter_count=0
 # Different expression: reconstruct a coordinate on the conic first.
 for n in range(1,H+1):
  for m in range(-H,H+1):
   if gcd(m,n)!=1:continue
   parameter_count+=1;t=Fraction(m,n)
   if a*t*t==b:continue
   u=(a*t*t-2*a*t+b)/(a*t*t-b)
   x=(u*u-1)/a
   if x and x not in (a,b):found.add(x)
 xs=[Fraction(v['x']) for v in obj['vertices']]
 assert len(set(xs))==len(xs) and xs==sorted(found),(path,'vertex coverage')
 assert parameter_count==obj['parameters_enumerated']
 nums=[x.numerator for x in xs];dens=[x.denominator for x in xs]
 edges=[];adj=[set() for _ in xs];tested=0
 # N/D is a rational square iff N*D is an integer square (D>0).
 for i in range(len(xs)):
  p=nums[i];q=dens[i]
  for j in range(i+1,len(xs)):
   tested+=1;D=q*dens[j];N=p*nums[j]+D
   if N<0:continue
   K=N*D
   if K%64 not in RES64 or K%63 not in RES63:continue
   s=isqrt(K)
   if s*s==K:edges.append([i,j]);adj[i].add(j);adj[j].add(i)
 assert edges==obj['edges'],(path,'edge mismatch')
 counts={3:0,4:0};max_recorded=0
 def dfs(clique,candidates):
  if len(clique) in counts:counts[len(clique)]+=1
  if len(clique)==4:return
  while candidates:
   v=min(candidates);candidates.remove(v)
   dfs(clique+[v],candidates & adj[v])
 dfs([],set(range(len(xs))))
 assert counts[3]==len(obj['triangles']) and counts[4]==len(obj['K4'])
 assert tested==obj['pair_tests']
 canonical={k:v for k,v in obj.items() if k!='elapsed_seconds'}
 digest=hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return {'file':str(path.relative_to(path.parent.parent)), 'anchors':[a,b],'height':H,
  'vertices':len(xs),'edges':len(edges),'triangles':counts[3],'K4':counts[4],
  'all_parameter_values_regenerated':True,'all_pairs_independently_retested':tested,
  'canonical_graph_sha256':digest,'pass':True,'elapsed_seconds':round(time.monotonic()-start,4)}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--workers',type=int,default=4);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 paths=sorted(str(p) for p in a.results.glob('anchors_H*/anchor_*.json'));rows=[]
 with ProcessPoolExecutor(max_workers=a.workers) as ex:
  for r in ex.map(audit,paths):rows.append(r);print(json.dumps(r),flush=True)
 out={'schema':'computational-crosscheck-v1','independent_ai_agents':0,'native_proofloop_execution':False,
      'coverage':'Every saved graph: all vertices regenerated, all potential edges retested, triangles and K4 counted by DFS.',
      'graphs':len(rows),'total_pair_checks':sum(x['all_pairs_independently_retested'] for x in rows),
      'all_pass':all(x['pass'] for x in rows),'rows':rows}
 a.output.write_text(json.dumps(out,indent=2)+'\n')
