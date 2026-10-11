"""Small exact regression checks plus optional symbolic identities.
No network access; no independent AI agent or formal assistant is invoked.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
from math import gcd,isqrt
import argparse,json,sys
from core import square_certificate,sqrtq,torsion_polynomial,dkms

def main(out, symbolic=False):
 cases={
 'piezas_one_integer':['34440','23001/280','840/68921','1121/11480','19383/1640','2530/287'],
 'gibbs_no_integer':['11/192','35/192','155/27','512/27','1235/48','180873/16'],
 'four_integer_quintuple':['1','3','8','120','777480/8288641'],
 'opposite_integer_quadruple':['-1','1','-24/25','24/25'],
 'nonsquare_denominator':['7','329','360/12943'],
 'dkms_t2':[str(x) for x in dkms(2)]}
 certs={name:square_certificate(xs) for name,xs in cases.items()}
 checks=[]
 for name,cert in certs.items():
  assert cert['distinct'] and cert['nonzero'] and all(e['root'] is not None for e in cert['pairs'])
  # Verify supplied roots independently by cross multiplication.
  xs=list(map(Q,cert['elements']))
  for e in cert['pairs']:
   x,y=xs[e['i']],xs[e['j']];r=Q(e['root'])
   assert r.numerator**2*x.denominator*y.denominator == r.denominator**2*(x.numerator*y.numerator+x.denominator*y.denominator)
  checks.append({'name':name,'pair_count':len(cert['pairs']),'integer_count':cert['integer_count'],'pass':True})
 assert certs['piezas_one_integer']['integer_count']==1
 assert certs['four_integer_quintuple']['integer_count']==4
 assert len(certs['four_integer_quintuple']['elements'])==5
 assert Q('360/12943').denominator==7*43**2
 assert isqrt(12943)**2!=12943
 # Invalid candidate with fifteen square tests: zero and distinctness still fail.
 rejected=square_certificate([6,8,Q(-1,8),Q(15,8),0,0])
 assert all(e['root'] is not None for e in rejected['pairs'])
 assert not rejected['distinct'] and not rejected['nonzero']
 xs=list(map(Q,cases['dkms_t2']))
 idxs=[list(idx) for idx in combinations(range(6),3) if torsion_polynomial(*(xs[i] for i in idx))==0]
 assert idxs==[[0,1,2]]
 algebra=[]
 if symbolic:
  import sympy as s
  a,b,t,A,B,z,U,V,h=s.symbols('a b t A B z U V h')
  D=a*t*t-b;u=(a*t*t-2*a*t+b)/D;v=(-a*t*t+2*b*t-b)/D
  x=4*t*(t-1)*(b-a*t)/D**2
  tests={'conic_ax':a*x+1-u*u,'conic_bx':b*x+1-v*v}
  T=4*(1+z*z)*V-U*U*z*z+12*z*z+6*U*z+3
  R2=1+V+U*z+z*z
  tests['doubling_identity']=(3+2*V+U*z)**2-4*R2*(V+3)+T
  tests['square_identity']=(2*z*z+U*z-1)**2-4*(1+z*z)*R2+T
  P=z**4-2*A*B*z**3+(A*A*B*B-4*B**3-12*B*B-6*B)*z*z-(6*A*B*B+4*A*B)*z-4*B**3-3*B*B
  tests['monic_polynomial']=P+B*B*T.subs({U:A+z/B,V:B+A*z/B})
  a0=2*h*h-2;b0=2*h*h;c0=-1/b0;d0=(2*b0-1)/b0
  tests['degenerate_quadruple_condition']=(a0*b0*c0*d0-3)**2-4*(a0*b0+c0*d0+3)
  tests['degenerate_constant']=2*a0*b0*c0+a0+b0+c0-d0
  for name,expr in tests.items():
   assert s.cancel(expr)==0,name
   algebra.append({'identity':name,'exact_residual':'0','pass':True})
 result={'schema':'exact-regression-v1','all_pass':True,'symbolic_requested':symbolic,'symbolic_engine':'SymPy '+s.__version__ if symbolic else None,
  'checks':checks,'symbolic_identities':algebra,'positive_controls':certs,
  'rejected_zero_duplicate_candidate':rejected,'dkms_t2_torsion_triples':idxs,
  'scope':'Exact finite controls and optional formal polynomial identities; not formal theorem-prover certification.'}
 out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'all_pass':True,'controls':len(certs),'symbolic_identities':len(algebra)}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--symbolic',action='store_true');a=p.parse_args();main(a.output,a.symbolic)
