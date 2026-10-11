# Auxiliary results for rational D(1) sextuples with two integer elements

Status: complete arguments authored and sequentially reviewed in one host session.
No independent AI review, external referee review, or formal proof-assistant check is asserted.
These results do not settle the main existence question. No priority claim is made.

## Definitions

A rational D(1) m-tuple is a set of m distinct nonzero rational numbers whose pairwise products, increased by 1, are rational squares. Zero is allowed as a square root, but not as an element of the set. We distinguish positive tuples from tuples of arbitrary signs.

## L1. Reduction of the signs of the integer anchors

Suppose a D(1) tuple contains two integer elements of opposite signs. Their product is an integer at most -1. Since their product plus 1 is a rational square, that product is at least -1. Hence the product equals -1, so the pair is {-1,1}.

Negating every element preserves every pairwise product. Consequently the arbitrary-sign target reduces to positive integer anchors 0<a<b with ab+1 an integer square, together with the exceptional anchor pair {-1,1}. This does not assert that the remaining four elements are positive.

For the exceptional pair, each additional element x must satisfy 1+x and 1-x square. Thus -1<x<1 once the two anchors themselves are excluded. No third distinct nonzero integer can occur in a tuple containing both anchors.

## L2. Complete rational parametrization of common neighbors

Let a,b be distinct nonzero rational numbers. Define

    D(t) = a*t^2-b,
    X(t) = 4*t*(t-1)*(b-a*t)/D(t)^2,
    U(t) = (a*t^2-2*a*t+b)/D(t),
    V(t) = (-a*t^2+2*b*t-b)/D(t).

Whenever D(t) is nonzero, direct expansion gives aX(t)+1=U(t)^2 and bX(t)+1=V(t)^2.

Conversely, let x be nonzero and suppose ax+1=u^2, bx+1=v^2 with u,v rational. Then u cannot be either 1 or -1. Set t=(v-1)/(u-1). The conic equation b*u^2-a*v^2=b-a becomes

    (u-1)*[(b-a*t^2)*(u-1)+2*(b-a*t)] = 0.

The first factor is nonzero. If a*t^2=b, the remaining equation forces a*t=b. Since a,b are nonzero, these equalities imply t=1 and a=b, a contradiction. Therefore D(t) is nonzero, and solving the displayed linear equation in u-1 gives precisely U(t), V(t), and X(t). There is no missing nonzero neighbor at t=infinity: the slope just defined is finite for every x under consideration.

Writing t=m/n in lowest terms with n>0 gives

    D = a*m^2-b*n^2,
    N = 4*m*n*(m-n)*(b*n-a*m),
    x = N/D^2.

For integer a,b this is an integer-arithmetic parametrization, even though cancellation can leave a nonsquare reduced denominator.

If ab+1 is square, form a graph with all common neighbors x other than 0,a,b as vertices, and join x,y exactly when xy+1 is square. A rational D(1) sextuple containing a,b exists if and only if this infinite graph contains K4. The equivalence is immediate in both directions from the fifteen defining equations. Restricting |m| and n gives a finite induced subgraph, not the entire graph.

## L3. Denominator support and its limitation

Let a,b be distinct nonzero integers, and let x=u/v be a common neighbor in lowest terms, v>0. Since gcd(u,v)=1,

    gcd(a*u+v,v) = gcd(a,v).

Thus the reduced denominator of ax+1 is v/gcd(a,v). The numerator and denominator of a reduced rational square are both integer squares, so v/gcd(a,v) is square. The same assertion holds with b in place of a.

In particular every prime occurring to an odd exponent in v divides gcd(a,b). If gcd(a,b)=1, then v is a perfect square. More precisely, if e=v_p(v), alpha=v_p(a), beta=v_p(b), both e-min(e,alpha) and e-min(e,beta) must be even.

The coprimality assumption cannot be dropped. For

    a=7, b=329, x=360/12943,

one has ab+1=48^2, ax+1=(47/43)^2, and bx+1=(137/43)^2, whereas 12943=7*43^2 is not a square.

## L4. The canonical order-three seed cannot contain two integers

**Proposition.** Let {a,b,c} be a rational D(1) triple. On

    E: Y^2=(X+ab)(X+ac)(X+bc),

let S=(1,R), where R^2=(ab+1)(ac+1)(bc+1). If S has order exactly 3, at most one of a,b,c is an integer.

The three roots of the cubic are distinct because a,b,c are distinct and nonzero, so E is nonsingular. The order assumption implies R is nonzero. Put

    z=abc, U=a+b+c, V=ab+ac+bc.

Then the cubic equals X^3+V*X^2+U*z*X+z^2 and

    R^2=1+V+U*z+z^2.

The tangent at S has slope (3+2V+Uz)/(2R). Since 2S=-S, its doubling formula gives

    (3+2V+Uz)^2 - 4*R^2*(V+3) = 0.

Expanding the left side yields -T, where

    T = 4*(1+z^2)*V-U^2*z^2+12*z^2+6*U*z+3.

Consequently T=0. A second direct identity is

    (2*z^2+U*z-1)^2-4*(1+z^2)*R^2 = -T.

Since R is nonzero, this proves that 1+z^2 is a rational square.

Assume for contradiction that a,b are integers. Write A=a+b and B=ab, so A,B are integers and B is nonzero. Substituting U=A+z/B and V=B+A*z/B into T=0, and multiplying by -B^2, gives

    z^4 - 2*A*B*z^3
    + (A^2*B^2-4*B^3-12*B^2-6*B)*z^2
    - (6*A*B^2+4*A*B)*z - 4*B^3-3*B^2 = 0.

This is monic with integer coefficients. The rational root theorem forces z to be an integer. It is nonzero because a,b,c are nonzero. We have just proved that z^2+1 is a rational square, hence an integer square. But

    |z|^2 < z^2+1 < (|z|+1)^2

for every nonzero integer z. This is impossible, completing the proof.

**Exact scope.** The assertion concerns the specified canonical point S, not every elliptic curve possessing some point of order 3. In the DKMS sextuple construction it excludes two integers in the seed triple. It does not exclude integers among the three appended coordinates, or one in each group. It therefore does not settle the sextuple question. The known order-three identity appears in DKMS, arXiv:1507.00569, Lemma 1 and Sections 2-3; the above integrality argument is supplied in full rather than inferred from a finite computation.

## L5. A whole family of false positives in the quadruple extension test

For each integer s>=2, put

    b=2*s^2, a=b-2, c=-1/b, d=(2*b-1)/b.

These four numbers are distinct and nonzero. Roots for ab+1, ac+1, ad+1, bc+1, bd+1, cd+1, respectively, are

    b-1, 1/s, (b-1)/s, 0, 2*s, (b-1)/b.

They satisfy (abcd-3)^2=4(ab+cd+3). In the extension equation recalled in DKP, Section 2,

    ((abcd-1)*x + 2abc+a+b+c-d)^2
        =4*(ab+1)*(ac+1)*(bc+1)*(d*x+1),

both 2abc+a+b+c-d and the product on the right are zero. Meanwhile abcd-1=-2*(b-1)^2/b is nonzero. The equation therefore reduces to x^2=0, so both appended roots are zero.

Thus these quadruples pass the preliminary identity but do not produce sextuples. Merely checking the fifteen product-plus-one square conditions on a six-position list would incorrectly accept them; nonzero and distinctness checks are essential. The actual search found s=2,3,4,5 in this family. Nothing here asserts that these quadruples have no other possible rational extensions.

## Remaining main-goal obligations

No six-element witness with two integers has been found. No all-anchor, unbounded-height K4 obstruction has been proved. No general rational-extension theorem establishes that the tested candidate mechanisms are exhaustive. The order-three seed obstruction does not cover the other coordinate placements in a sextuple. These are obligations for the original target, not missing steps in L1-L5.
