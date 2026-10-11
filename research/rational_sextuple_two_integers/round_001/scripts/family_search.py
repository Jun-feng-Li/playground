"""Exact finite specialization of two cited, explicitly specified families."""
from core import dkms,dkp_square_family,square_certificate
from fractions import Fraction as Q
from math import gcd
from pathlib import Path
import json,time,argparse
from collections import Counter

def main(H,out):
 start=time.monotonic();rows=[];hits=[];failed=[];boundary=[]
 parameters=[Q(m,n) for n in range(1,H+1) for m in range(1,H+1) if gcd(m,n)==1 and m!=n]
 for label,fun in [('DKMS_k3',lambda t:dkms(t,3)),('DKMS_k5',lambda t:dkms(t,5)),('DKP_F',dkp_square_family)]:
  hist=Counter();verified=0;invalid=0
  for t in parameters:
   xs=fun(t)
   if xs is None:invalid+=1;continue
   cert=square_certificate(xs)
   if not cert['distinct'] or not cert['nonzero']:invalid+=1;continue
   if any(p['root'] is None for p in cert['pairs']):failed.append({'family':label,'t':str(t),'certificate':cert});continue
   verified+=1;hist[cert['integer_count']]+=1
   if cert['integer_count']>=1:hits.append({'family':label,'t':str(t),'certificate':cert})
  rows.append({'family':label,'parameter_count':len(parameters),'valid_sextuples_verified':verified,'degenerate_specializations':invalid,'integer_count_histogram':dict(hist)})
 report={'schema':'family-specialization-v1','height':H,'parameters':'t=m/n, 1<=m,n<=H, gcd(m,n)=1, m!=n; k as listed','rows':rows,'integer_hits':hits,'arithmetic_failures':failed,'scope':'finite family specializations only; no global nonexistence inference','elapsed_seconds':round(time.monotonic()-start,4)}
 Path(out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['integer_hits','arithmetic_failures']},indent=2));print('integer hits',len(hits),'errors',len(failed))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--height',type=int,default=60);p.add_argument('--output',required=True);a=p.parse_args();main(a.height,a.output)
