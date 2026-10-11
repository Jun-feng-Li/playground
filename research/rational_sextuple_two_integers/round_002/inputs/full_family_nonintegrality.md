# A full-height nonintegrality theorem for one explicit rational family

Provenance: newly authored by the coordinating research host. This is a proposed mathematical proof, not a previously accepted ProofLoop lemma, an independent-model verdict, a formal proof-assistant certificate, or a claim of priority. Its full argument is supplied for independent reconstruction and review. No assertion about all rational Diophantine sextuples is made.

## Definitions and theorem

Let t=m/n be a rational number in lowest terms, with n>0, m nonzero, and m^2 != n^2. Put H=m^2+n^2, D=m^2-n^2, and Q=m^4+34m^2n^2+n^4. Define

 a=-9H/(8D),
 b=(m^2-7n^2)H(7m^2-n^2)/(8D^3),
 c=8D^3/(9H^3),
 e=-2(m^2+5n^2)(5m^2+n^2)/(9DH),
 f=-2mn(m^2-4mn-3n^2)(3m^2-4mn-n^2)(m^3+8m^2n+5mn^2+4n^3)(4m^3-5m^2n+8mn^2-n^3)/(DHQ^2),
 g=2mn(m^2+4mn-3n^2)(3m^2+4mn-n^2)(m^3-8m^2n+5mn^2-4n^3)(4m^3+5m^2n+8mn^2+n^3)/(DHQ^2).

**Theorem.** None of a,b,c,e,f,g is an integer, for every such m,n, with no height bound. Moreover Q has a prime divisor p>3. Every such divisor satisfies p=1 modulo 8 and

 v_p(f)=v_p(g)=-2 v_p(Q).

In particular, both last reduced denominators are divisible by the square of a common prime p>=17 congruent to 1 modulo 8. Here v_p(x) is the exponent of p in a nonzero rational number. This theorem excludes only this displayed formula family as a source of tuples containing integers; it does not settle the original two-integer sextuple existence problem.

## Proof: first four coordinates

Since gcd(m,n)=1, either m,n have opposite parity, or both are odd. In the first case H,D,m^2-7n^2,7m^2-n^2 are odd. In particular all these factors are nonzero, and v_2(a)=v_2(b)=-3. In the second case odd squares are 1 modulo 8, so v_2(H)=1, v_2(D)>=3, and v_2(m^2-7n^2)=v_2(7m^2-n^2)=1. The last two residues are 2 and 6 modulo 8; D is nonzero by the domain assumption. Thus

 v_2(a)=1-3-v_2(D)<0,
 v_2(b)=1+1+1-3-3v_2(D)=-3v_2(D)<0.

A nonzero integer has nonnegative p-adic valuation, proving the assertion for a and b in every primitive parity case. All factors considered are nonzero by the same residue arguments.

Both m^2 and n^2 are positive. Consequently 0<|D|<H, and 0<|c|=(8/9)(|D|/H)^3<1. Thus c is not an integer.

If e were an integer, its displayed integer denominator 9DH would divide its displayed integer numerator N=-2(m^2+5n^2)(5m^2+n^2). This necessary condition holds even before reduction: if N/(9DH)=k with k integral, then N=k(9DH). Hence H divides N. Reducing m^2=-n^2 modulo H gives N=32n^4 modulo H. Since gcd(H,n)=gcd(m^2+n^2,n)=1, it follows that H divides 32. But primitive parity gives v_2(H)=0 or 1; therefore H, if a positive divisor of 32, would have to be 1 or 2. Nonzero unequal absolute values of m,n give H>=5, a contradiction. This proves e is nonintegral without an assumption that its displayed fraction was already reduced.

## Proof: a prime of Q beyond 2 and 3

A prime dividing Q cannot divide m or n, because substitution of m=0 or n=0 modulo that prime and gcd(m,n)=1 would make Q a nonzero fourth power.

If m,n have opposite parity, Q is odd. If both are odd, m^4=n^4=1 modulo 16 and m^2 n^2 is 1 or 9 modulo 16. Since 34=2 modulo 16, in either case Q=4 modulo 16. Thus v_2(Q) is respectively 0 or 2.

If 3 divides mn, primitive coprimality shows Q=1 modulo 3, hence v_3(Q)=0. Otherwise both m^2,n^2 equal 1 modulo 3. Write D=3k. The exact identity Q=D^2+36m^2n^2 gives

 Q=9(k^2+4m^2n^2).

Modulo 3 the parenthesis equals k^2+1, which is 1 or 2, never zero. Hence v_3(Q)=2 in this case.

Were 2 and 3 the only prime divisors of Q, the two valuation computations would imply Q divides 2^2 3^2=36. However at least one of |m|,n is >=2 and the other is >=1, so Q>=16+34*4+1=153. This contradiction proves the existence of a prime divisor p>3.

## Five exact polynomial identities

Write q(T)=T^4+34T^2+1, and set
 P1=T^2-4T-3,
 P2=3T^2-4T-1,
 P3=T^3+8T^2+5T+4,
 P4=4T^3-5T^2+8T-1.

The following are identities in Z[T], established by polynomial multiplication and collecting coefficients:

 q+(-T^3-34T)T=1;
 (33-7T)q+(7T^3-5T^2+239T-181)P1=576;
 (197-123T)q+(41T^3-11T^2+1393T-379)P2=576;
 (17T^2+123T-20)q+(-17T^3+13T^2-577T+437)P3=1728;
 (628T^2-717T+1151)q+(-157T^3-17T^2-5333T-577)P4=1728.

For explicit checks, the following pairs are the coefficient vectors of the two summands in each of the last four identities, in ASCENDING degree order. Each pair adds to [C,0,...,0]:

 C=576: [33, -7, 1122, -238, 33, -7] + [543, 7, -1122, 238, -33, 7]
 C=576: [197, -123, 6698, -4182, 197, -123] + [379, 123, -6698, 4182, -197, 123]
 C=1728: [-20, 123, -663, 4182, 558, 123, 17] + [1748, -123, 663, -4182, -558, -123, -17]
 C=1728: [1151, -717, 39762, -24378, 22503, -717, 628] + [577, 717, -39762, 24378, -22503, 717, -628]

These vectors follow by the elementary convolution formula for polynomial multiplication. Thus each displayed identity can be checked by distributivity and exact integer arithmetic. No numerical approximation or reported resultant is a premise.

## Proof: exclusion of numerator cancellation and the last two coordinates

Fix any prime p>3 dividing Q. Since p does not divide n, set T=m/n in F_p. Then q(T)=Q/n^4=0. Neither 576=2^6*3^2 nor 1728=2^6*3^3 vanishes in F_p. The four identities imply that none of P1(T),P2(T),P3(T),P4(T) is zero. Also p does not divide 2mn. Homogenizing each factor multiplies its evaluation by n^2 or n^3, which is a unit modulo p. Thus the integer numerator of f is nonzero modulo p.

Since Q=D^2+36m^2n^2=H^2+32m^2n^2 and p>3 does not divide mn, p can divide neither D nor H. Hence the p-adic valuation of the displayed denominator DHQ^2 is exactly 2v_p(Q), whereas the numerator valuation is zero. It follows that v_p(f)=-2v_p(Q)<0. In particular f is nonzero and nonintegral; a zero numerator is also excluded by its nonzero residue modulo p.

Replacing m by -m preserves H,D,Q and primitive admissibility. In the formula for f the prefactor -2mn becomes 2mn. The two quadratic factors become the corresponding plus factors in g. Each cubic becomes the negative of the corresponding cubic in g; these two signs cancel. Therefore g(m,n)=f(-m,n) exactly. Applying the same argument at (-m,n) gives v_p(g)=-2v_p(Q)<0. No sign restriction on m has been imposed.

## Proof: the prime congruence

For the same p, all denominators in

 r=D/(6mn), s=H/(4mn)

are invertible modulo p. The two norm identities for Q give r^2=-1 and s^2=-2 in F_p. Therefore u=s/r has u^2=2. Put z=u(1+r)/2. Its square is z^2=2(1+2r+r^2)/4=r, so z^4=-1 and z^8=1. Since p is odd, -1 is not 1, so z has multiplicative order exactly 8. The order of an element of F_p^* divides p-1, whence p=1 modulo 8. The least prime in this class is 17. This finishes all assertions.

## Exact scope

All arguments concern every primitive integer pair in the stated domain, not a bounded search. The theorem does not assert that these formulas exhaust rational D(1) sextuples or any integer-anchor pairs. Neither the unrestricted-sign nor the all-positive main existence question is solved. The identity certificate is elementary arithmetic, not a formal proof-assistant verification. Independent role review and native acceptance must be recorded separately from this host-authored proof.
