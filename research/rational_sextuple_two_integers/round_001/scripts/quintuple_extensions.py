"""Heuristic extensions of every saved anchored quintuple.
Candidates come from regular triples, regular quadruples and the explicit
quadratic recalled in DKP Section 2. All six-element outputs are checked
from their definitions; no claimed completeness beyond this candidate set.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
from core import sqrtq,square_certificate
import json,time,argparse,hashlib

def run(root,out):
 start=time.monotonic();quints={}
 for path in sorted(root.glob('anchors_H*/anchor_*.json')):
  doc=json.loads(path.read_text());ab=list(map(Q,doc['anchors']));xs=[Q(v['x']) for v in doc['vertices']]
  for tri in doc['triangles']:
   quint=tuple(sorted(ab+[xs[i] for i in tri]));quints.setdefault(quint,{'file':str(path.relative_to(root)),'triangle':tri})
 candidates_count=0;tested=0;found=[];stats={};input_has_four_integers=0;largest=[]
 for xs,origin in sorted(quints.items()):
  if sum(x.denominator==1 for x in xs)>=4:input_has_four_integers+=1
  cand={}
  for a,b in combinations(xs,2):
   s=sqrtq(a*b+1)
   assert s is not None
   for v in (a+b+2*s,a+b-2*s):cand.setdefault(v,'pair_regular')
  for a,b,c in combinations(xs,3):
   s=sqrtq((a*b+1)*(a*c+1)*(b*c+1));assert s is not None
   for v in (a+b+c+2*a*b*c+2*s,a+b+c+2*a*b*c-2*s):cand.setdefault(v,'triple_regular')
  for a,b,c,d in combinations(xs,4):
   K=a*b*c*d-1;C=2*a*b*c+a+b+c-d;F=(a*b+1)*(a*c+1)*(b*c+1)
   A=K*K;B=2*K*C-4*F*d;D=C*C-4*F
   if not A:
    if B:cand.setdefault(-D/B,'quadratic_linear_case')
    continue
   disc=B*B-4*A*D;s=sqrtq(disc)
   if s is None:continue
   for v in ((-B+s)/(2*A),(-B-s)/(2*A)):cand.setdefault(v,'quadruple_quadratic')
  candidates_count+=len(cand)
  for v,method in cand.items():
   if not v or v in xs:continue
   tested+=1;stats[method]=stats.get(method,0)+1
   if all(sqrtq(v*x+1) is not None for x in xs):
    cert=square_certificate(list(xs)+[v]);assert cert['distinct'] and cert['nonzero'] and cert['integer_count']>=2
    found.append({'origin':origin,'method':method,'certificate':cert})
  largest.append({'quintuple':list(map(str,xs)),'origin':origin,'distinct_generated_candidates':len(cand)})
 result={'schema':'quintuple-extensions-v1','scope':'Only the three specified candidate mechanisms, on all distinct quintuples in the saved graphs. Candidates are not bounded in height. This is not an exhaustive rational extension algorithm.',
 'distinct_input_quintuples':len(quints),'inputs_with_at_least_four_integers':input_has_four_integers,
 'distinct_candidates_per_input_sum':candidates_count,'nonzero_new_candidates_checked':tested,'candidate_counts_by_first_method':stats,
 'sextuple_witnesses':found,'inputs':largest,'elapsed_seconds':round(time.monotonic()-start,4)}
 out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='inputs'},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.results,a.output)
