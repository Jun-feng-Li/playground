# Continuation research input: exact family integrality

This is a host-authored research proposal, not an accepted theorem or an external peer review. Its formulas are the homogeneous rewrite of dkp_square_family in round_001/scripts/core.py. That program defines the formulas; its finite evaluations do not prove any all-height assertion, Diophantine property, or exhaustiveness.

The main question remains whether six distinct nonzero rationals, including at least two integers, can have all fifteen pairwise products plus one rational squares. All-positive and unrestricted-sign cases remain separate. Excluding this single family does not answer that main question.

## Exact family

Let m,n be relatively prime integers, n>0, m nonzero, and m^2 != n^2. Thus t=m/n is any rational parameter other than 0,1,-1. Put

H=m^2+n^2,
D=m^2-n^2,
Q=m^4+34*m^2*n^2+n^4.

Define six rational values:

A=-9*H/(8*D),
B=(m^2-7*n^2)*H*(7*m^2-n^2)/(8*D^3),
C=8*D^3/(9*H^3),
E=-2*(m^2+5*n^2)*(5*m^2+n^2)/(9*D*H),
Fminus=-2*m*n*(m^2-4*m*n-3*n^2)*(3*m^2-4*m*n-n^2)*(m^3+8*m^2*n+5*m*n^2+4*n^3)*(4*m^3-5*m^2*n+8*m*n^2-n^3)/(D*H*Q^2),
Fplus=2*m*n*(m^2+4*m*n-3*n^2)*(3*m^2+4*m*n-n^2)*(m^3-8*m^2*n+5*m*n^2-4*n^3)*(4*m^3+5*m^2*n+8*m*n^2+n^3)/(D*H*Q^2).

Research target: prove or disprove that none of these six values is an integer for any admissible m,n. This would strictly upgrade the previous finite family search to an unbounded-height exclusion of this explicit family. It would not exclude other rational sextuples or all integer-anchor pairs. Do not assert priority or novelty without a separate literature audit.

## Suggested avenues, to check rather than assume

1. For A and B, split the primitive parity cases (opposite parity; both odd) and compute exact 2-adic valuations.
2. For C, compare |D| with H over the reals.
3. For E, use gcd(H,m*n)=1 and reduce its numerator modulo H; integrality might force H to divide a small power of 2.
4. For the last two values, a prime p dividing Q cannot divide m*n. Test the resultants between q(T)=T^4+34*T^2+1 and each numerator factor T, T^2-4*T-3, 3*T^2-4*T-1, T^3+8*T^2+5*T+4, and 4*T^3-5*T^2+8*T-1. A host exact SymPy calculation gave respectively 1,18432,18432,1492992,1492992. These are supplied as candidate identities requiring independent derivation, explicit Bezout certificates, or an exact reproducible calculation; do not treat the reported numbers as a proved lemma.
5. Explore whether integrality of either last coordinate forces every prime divisor of Q into {2,3}. If so, rigorously determine v_2(Q) and v_3(Q) for every primitive pair, including all signs and residue classes. Compare with the minimum possible Q. Cancellation must be justified before any denominator claim.
6. The substitution m -> -m interchanges the last two formulas. Check its precise sign and coordinate action before using symmetry.

## Scope and review rules

Each prover must submit its exact mathematical assertion and a standalone proof. Use gaps only for missing steps inside that assertion; put unsolved portions of the original sextuple question in method_summary. A partial claim may have no proof gaps while the original goal stays open.

Every reviewer must check the actual submitted proof, all parity/valuation cases, prime-divisor cancellation, signs, exceptional parameters and the finite-versus-infinite distinction. Give substantive explanations in confirmed_fragments; block an unsupported computational identity or missing quantified case. Do not silently supply an essential missing proof on behalf of the author.

All role tasks must use distinct provider sessions with genuine execution receipts. Same-host arithmetic checks are supplementary and must never be described as independent AI reviews.
