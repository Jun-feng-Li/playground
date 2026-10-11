from fractions import Fraction as Q
from math import isqrt
from itertools import combinations

def sqrtq(x):
 x=Q(x)
 if x<0:return None
 p,q=isqrt(x.numerator),isqrt(x.denominator)
 return Q(p,q) if p*p==x.numerator and q*q==x.denominator else None

def square_certificate(xs):
 xs=list(map(Q,xs));return {'elements':list(map(str,xs)),'distinct':len(set(xs))==len(xs),'nonzero':all(xs),'integer_count':sum(x.denominator==1 for x in xs),'pairs':[{'i':i,'j':j,'product_plus_one':str(xs[i]*xs[j]+1),'root':None if sqrtq(xs[i]*xs[j]+1) is None else str(sqrtq(xs[i]*xs[j]+1))} for i,j in combinations(range(len(xs)),2)]}

def torsion_polynomial(a,b,c):
 z=a*b*c;A=a+b+c;B=a*b+a*c+b*c
 return (4+4*z*z)*B-A*A*z*z+12*z*z+6*A*z+3

def ec_add(P,Q_,A2,A4):
 if P is None:return Q_
 if Q_ is None:return P
 x,y=P;u,v=Q_
 if x==u:
  if y+v==0:return None
  m=(3*x*x+2*A2*x+A4)/(2*y)
 else:m=(v-y)/(u-x)
 w=m*m-A2-x-u
 return (w,m*(x-w)-y)

def dkms(t,k=3):
 t=Q(t)
 if t in (0,1,-1):return None
 u=t*t-6*t+1;v=t*t+6*t+1
 if not u*v:return None
 a=18*t*(t*t-1)/(u*v)
 b=(t-1)*v*v/(6*t*(t+1)*u)
 c=(t+1)*u*u/(6*t*(t-1)*v)
 A2=a*b+a*c+b*c;A4=a*b*c*(a+b+c);z=a*b*c
 rs=sqrtq((a*b+1)*(a*c+1)*(b*c+1))
 if rs is None:raise ValueError('not rational S')
 P=(Q(0),z); S=(Q(1),rs);T=None
 for _ in range(k):T=ec_add(T,P,A2,A4)
 if T is None:return None
 U=ec_add(T,S,A2,A4);V=ec_add(T,(S[0],-S[1]),A2,A4)
 if U is None or V is None:return None
 return [a,b,c,T[0]/z,U[0]/z,V[0]/z]

if __name__=='__main__':
 import json
 xs=dkms(2);print(xs)
 print('torsion triples',[idx for idx in combinations(range(6),3) if torsion_polynomial(*(xs[i] for i in idx))==0])
 xs=list(map(Q,['34440','23001/280','840/68921','1121/11480','19383/1640','2530/287']))
 print('Piezas torsion triples',[idx for idx in combinations(range(6),3) if torsion_polynomial(*(xs[i] for i in idx))==0])
 print(json.dumps(square_certificate(xs),indent=2))

def dkp_square_family(t):
 t=Q(t)
 if t in (1,-1):return None
 d=t*t-1;h=t*t+1;v=t**4+34*t*t+1
 a=-9*h/(8*d)
 b=(t*t-7)*h*(7*t*t-1)/(8*d**3)
 c=8*d**3/(9*h**3)
 e=-2*(t*t+5)*(5*t*t+1)/(9*d*h)
 f=-2*t*(t*t-4*t-3)*(3*t*t-4*t-1)*(t**3+8*t*t+5*t+4)*(4*t**3-5*t*t+8*t-1)/(d*h*v*v)
 g=2*t*(t*t+4*t-3)*(3*t*t+4*t-1)*(t**3-8*t*t+5*t-4)*(4*t**3+5*t*t+8*t+1)/(d*h*v*v)
 return [a,b,c,e,f,g]
