"""DKP condition on every enumerated anchored quadruple, all three pairings.
The extra two elements, if rational, are not restricted to the parameter box.
"""
from pathlib import Path
from fractions import Fraction as Q
from core import sqrtq,square_certificate
import json,time,argparse

def run(root,out):
 start=time.monotonic();nquad=0;nchecks=0;hits=[];candidates=[];rows=[]
 for path in sorted(root.glob('anchors_H*/anchor_*.json')):
  obj=json.loads(path.read_text());a,b=map(Q,obj['anchors']);xs=[Q(v['x']) for v in obj['vertices']];count=0
  for i,j in obj['edges']:
   c,d=xs[i],xs[j];W=a*b*c*d;target=(W-3)**2/4-3;nquad+=1
   for aa,bb,cc,dd in [(a,b,c,d),(a,c,b,d),(a,d,b,c)]:
    nchecks+=1
    if target!=aa*bb+cc*dd:continue
    count+=1;rec={'file':str(path.relative_to(root)),'edge':[i,j],'ordered_quadruple':list(map(str,[aa,bb,cc,dd]))}
    C=2*aa*bb*cc+aa+bb+cc-dd;K=W-1;F=(aa*bb+1)*(aa*cc+1)*(bb*cc+1)
    A=K*K;B=2*K*C-4*F*dd;D=C*C-4*F
    rec['quadratic_coefficients']=list(map(str,[A,B,D]))
    disc=B*B-4*A*D;s=sqrtq(disc)
    if not A:rec['status']='degenerate_quadratic'
    elif s is None:rec['status']='nonsquare_discriminant'
    else:
     e=(-B+s)/(2*A);f=(-B-s)/(2*A)
     cert=square_certificate([aa,bb,cc,dd,e,f]);rec['certificate']=cert
     rec['status']='valid_sextuple' if cert['distinct'] and cert['nonzero'] and all(z['root'] is not None for z in cert['pairs']) else 'rejected_degenerate_or_nonsquare'
     if rec['status']=='valid_sextuple':candidates.append(rec)
    hits.append(rec)
  rows.append({'file':str(path.relative_to(root)),'quadruples':len(obj['edges']),'condition_hits':count})
 result={'schema':'dkp-quadruple-route-v1','source':'arXiv:1903.02805, Section 2, equation (1) and the following extension equation; it cites Proposition 1 of reference [3]',
 'scope':'Every edge in the saved finite anchor graphs, all three pairings. Appended roots unrestricted in height. Not all rational quadruples.',
 'quadruples_tested_with_repetition':nquad,'pairing_conditions_tested':nchecks,'condition_hits':hits,'sextuple_candidates':candidates,'rows':rows,'elapsed_seconds':round(time.monotonic()-start,4)}
 out.write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='rows'})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.results,a.output)
