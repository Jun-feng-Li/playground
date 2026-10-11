# Real ProofLoop role task: problem intake

This task was created and claimed by an actually running ProofLoop 0.19.34 stdio MCP controller. It is not a request to simulate multiple roles. The independent execution policy is `adapter_verified`; no role output has yet been authored, signed or submitted. The private runtime source repository `Jun-feng-Li/proofloop` remains read-only and is not copied here.

## Immutable task binding

- Run: `run_2dde091dc2bc4733918344c78de56b06`
- Job: `job_13cad664eb8f41d09be85595b8ab9634`, generation 1
- Role: `briefing_builder`
- Scope: `problem_intake`
- Input SHA-256: `6251c240119a4165cff268daaf055b4484956a408f2cc6a4d3066173f72920dc`
- Problem SHA-256: `15447bb24a0ff99031c47eef2e46240ca130900d166b830e44e1956eebefa833`

## Assigned work

Convert the supplied raw problem into a ProblemContract, preserving every hypothesis, quantifier and objective. Map each field to its original excerpt. Keep source_refs empty and the operator's acceptance_profile `reviewed`.

Complete only this intake role. Do not prove the theorem, accept previous claims, perform the subsequent verifier role, or claim controller acceptance. A later independent task must review this output. Do not modify prior research, workflows, runtime, credentials, or the reference repository.

## Complete original input

The following code block contains the original input artifact. Its bytes contain no trailing newline.

```text
Determine whether there exists a set S of six pairwise distinct nonzero rational numbers such that at least two elements of S are integers and, for every two distinct elements x,y of S, xy+1 is the square of a rational number. Track the all-positive subcase separately from the unrestricted-sign case. A zero square root is permitted; zero elements and repeated elements are forbidden. An existence answer must supply six exact rational values and all fifteen exact square roots, or a complete nondegenerate construction. A nonexistence answer must cover all rational heights and all allowable integer pairs; bounded searches and exclusions of specific constructions do not suffice. Previous work in round_001 is unreviewed input in this new independently reviewed run, not an accepted lemma. The user requires real ProofLoop tool execution with independent AI contexts for role tasks. Never substitute same-session role simulation, Python processes, or arithmetic CI for independent AI reviews. Keep Jun-feng-Li/proofloop read-only and archive research in Jun-feng-Li/playground.
```

Acknowledge the following complete reference only after actually reading the original input:

```json
{"media_type":"text/plain","object_id":"obj_dfd9831e2ce35271b47f8781d78630e5a7d2b8ad883d0896d0451b3367a02c0d","sha256":"fcd77da5e0801214c0796c5f1ecaba195c5c2ce0d7ba2f1476dea5d9470f2ff1","size_bytes":1080}
```

## Required result

Create only these two new files on this PR's branch, and do not merge the PR:

- `research/rational_sextuple_two_integers/round_002/agent_results/job_13cad664eb8f41d09be85595b8ab9634/output.json`
- `research/rational_sextuple_two_integers/round_002/agent_results/job_13cad664eb8f41d09be85595b8ab9634/notes.md`

`output.json` must have exactly these five top-level keys:

```json
{
  "problem_sha256": "15447bb24a0ff99031c47eef2e46240ca130900d166b830e44e1956eebefa833",
  "input_sha256": "6251c240119a4165cff268daaf055b4484956a408f2cc6a4d3066173f72920dc",
  "read_receipts": [],
  "usage": {"provider_requests": null, "total_tokens": null},
  "output": {}
}
```

Replace read_receipts with the complete reference to the input actually read. Leave usage counts null unless measured provider data are available; do not invent counts.

`output` has exactly two keys: `problem_contract` and `statement_mapping`.

`problem_contract` has exactly:
- `statement`: nonempty string;
- `assumptions`: array of unique nonempty strings;
- `quantifiers`: array of unique nonempty strings;
- `objective`: one of `proof`, `counterexample`, `bound_improvement`;
- `acceptance_profile`: `reviewed`;
- `source_refs`: [].

The objective enum is coarse: preserve the decision question faithfully in statement and explain the chosen objective in statement_mapping. Do not replace an existence decision by an unsupported nonexistence claim.

Each `statement_mapping` item has exactly `contract_field` (one of statement/quantifiers/assumptions/objective), `raw_excerpt` (exact substring of original input), and `explanation` (nonempty string). Cover all important hypotheses and quantifiers.

In notes.md, explain scope decisions and provide the actual provider task/session identifier when exposed. Otherwise state that it was not exposed. Never fabricate an independent context, a second reviewer, a provider execution count, or a successful ProofLoop submission. The external controller owns task settlement and downstream scheduling.
