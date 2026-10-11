"""Execute a batch of already-claimed ProofLoop jobs in separate provider sessions.

This is a transport adapter, not a replacement controller. It never fabricates
role outputs, changes the frozen claims, attests model correctness or submits
results. The external ProofLoop controller validates and settles actual returns.
"""
from __future__ import annotations
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import zlib


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def execute(task: dict, batch: str, output_root: Path) -> dict:
    card = task['card']
    job = card['job_id']
    directory = output_root / job
    directory.mkdir(parents=True, exist_ok=False)
    for item in task['artifacts']:
        raw = item['content_utf8'].encode('utf-8')
        reference = item['artifact']
        if digest(raw) != reference['sha256'] or len(raw) != reference['size_bytes']:
            raise ValueError('Artifact bytes do not match the frozen reference')
    required = {ref['object_id'] for ref in card['required_reads']}
    supplied = {item['artifact']['object_id'] for item in task['artifacts']}
    if not required <= supplied:
        raise ValueError('Required input artifact is missing')
    instructions = (
        'You are one independently executed ProofLoop role, in a fresh context. '
        'Complete ONLY the role and scope of the frozen task below. Follow its '
        'instructions, snapshot, exact submission schema and output template. '
        'Read every supplied required artifact before acknowledging it; copy each '
        'complete required_reads reference into read_receipts after reading. '
        'All required text is included here, so do not invoke tools or access files, '
        'environment variables or network resources. Do not impersonate other '
        'roles, the controller, an external expert or a formal proof assistant. '
        'Do not assume that an earlier attempt is true or accepted unless its '
        'actual recorded status says so. Finite computations establish only their '
        'stated finite scope. Supply substantive mathematical reasoning for each '
        'claim or review, identifying every unresolved obligation. Keep partial '
        'results separate from resolution of the main goal. Unsupported passes '
        'and invented citations are forbidden. Unknown measured usage values '
        'remain null. Return ONLY the complete JSON object required by the '
        'submission schema as your final answer, with no Markdown fences. '
        'The host will capture the real session identity, provider evidence and '
        'output bytes separately. Do not claim controller submission or acceptance.\n\n'
    )
    prompt = instructions + json.dumps(task, ensure_ascii=False, separators=(',', ':'))
    (directory / 'prompt.txt').write_text(prompt, encoding='utf-8')
    isolated = Path(os.environ['RUNNER_TEMP']) / ('proofloop-' + batch + '-' + job)
    isolated.mkdir(parents=True, exist_ok=False)
    argv = ['copilot', '-p', prompt, '--no-ask-user', '--no-custom-instructions', '--output-format=json']
    started = time.time()
    returncode = None
    failure = None
    try:
        completed = subprocess.run(argv, cwd=isolated, capture_output=True, timeout=600)
        stdout, stderr, returncode = completed.stdout, completed.stderr, completed.returncode
    except subprocess.TimeoutExpired as exc:
        stdout, stderr = exc.stdout or b'', exc.stderr or b''
        failure = 'provider_timeout_without_automatic_retry'
    secret = os.environ.get('GITHUB_TOKEN', '').encode()
    if secret:
        stdout = stdout.replace(secret, b'[REDACTED]')
        stderr = stderr.replace(secret, b'[REDACTED]')
    events = []
    invalid_lines = 0
    for line in stdout.splitlines():
        try:
            events.append(json.loads(line))
        except (ValueError, TypeError):
            invalid_lines += 1
    # Do not publish private reasoning, internal system prompts, encrypted
    # continuation state, cache details or streaming reasoning deltas.
    public = []
    finals = []
    results = []
    model_calls = 0
    tool_calls = 0
    metrics = None
    for event in events:
        kind = event.get('type')
        data = event.get('data') or {}
        if kind == 'model.call_start':
            model_calls += 1
        if kind == 'tool.execution_start':
            tool_calls += 1
        if kind == 'session.usage_checkpoint':
            metrics = data.get('accountingSnapshot', {}).get('modelMetrics')
        if kind == 'assistant.message' and data.get('phase') == 'final_answer':
            selected = {k: data[k] for k in ('messageId', 'model', 'providerId', 'content', 'interactionId', 'turnId', 'phase') if k in data}
            public.append({'type': kind, 'timestamp': event.get('timestamp'), 'data': selected})
            finals.append(selected)
        if kind == 'result':
            selected = {k: event[k] for k in ('type', 'timestamp', 'sessionId', 'exitCode', 'usage') if k in event}
            public.append(selected)
            results.append(selected)
        if kind in ('model.call_start', 'model.call_finished', 'model.call_final_result'):
            selected = {k: data[k] for k in ('model', 'modelId', 'providerId', 'requestId', 'interactionId', 'turnId', 'status', 'error', 'usage', 'durationMs') if k in data}
            public.append({'type': kind, 'timestamp': event.get('timestamp'), 'data': selected})
    public_raw = ''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in public).encode()
    (directory / 'provider_events_public.jsonl').write_bytes(public_raw)
    (directory / 'stderr.txt').write_bytes(stderr)
    model_response = returncode == 0 and len(finals) == 1 and len(results) == 1 and results[0].get('exitCode') == 0 and bool(results[0].get('sessionId'))
    output_hash = None
    if model_response:
        answer = finals[0]['content'].encode('utf-8')
        (directory / 'role_output.raw.txt').write_bytes(answer)
        output_hash = digest(answer)
        try:
            json.loads(answer)
            (directory / 'output.json').write_bytes(answer)
        except ValueError:
            failure = 'model_final_answer_is_not_exact_json'
    else:
        failure = failure or 'no_single_successful_provider_final_answer'
    receipt = {
        'schema': 'source-bound-external-role-v1', 'batch': batch,
        'run_id': card['run_id'], 'job_id': job, 'generation': card['generation'],
        'role': card['role'], 'scope': card['scope'], 'input_sha256': card['input_sha256'],
        'workflow_run_id': os.environ['GITHUB_RUN_ID'], 'workflow_attempt': os.environ['GITHUB_RUN_ATTEMPT'],
        'source_commit': os.environ['GITHUB_SHA'], 'backend': 'github-copilot-cli',
        'requested_model': 'provider-default', 'actual_model': finals[0].get('model') if finals else None,
        'session_id': results[0].get('sessionId') if len(results) == 1 else None,
        'model_call_count': model_calls, 'tool_call_count': tool_calls,
        'prompt_sha256': digest(prompt.encode()), 'original_redacted_stdout_sha256': digest(stdout),
        'original_redacted_stdout_bytes': len(stdout), 'public_events_sha256': digest(public_raw),
        'output_sha256': output_hash, 'exit_code': returncode, 'failure': failure,
        'elapsed_seconds': round(time.time() - started, 3), 'measured_model_metrics': metrics,
        'invalid_jsonl_line_count': invalid_lines,
        'fresh_process_without_session_resume': True,
        'provider_model_response_observed': model_response,
        'controller_submission_performed': False,
        'redaction': 'Only final role answer and selected provider execution metadata are retained; private reasoning and opaque continuation state are not published.'
    }
    (directory / 'execution_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    return {'job_id': job, 'provider_model_response_observed': model_response, 'failure': failure, 'session_id': receipt['session_id']}


def main() -> int:
    envelope = json.loads(Path(sys.argv[1]).read_text())
    raw = zlib.decompress(base64.b64decode(envelope['payload']))
    if len(raw) != envelope['uncompressed_size'] or digest(raw) != envelope['sha256']:
        raise ValueError('Dispatch bundle digest mismatch')
    bundle = json.loads(raw)
    if [t['card']['job_id'] for t in bundle['tasks']] != envelope['job_ids']:
        raise ValueError('Dispatch job identity mismatch')
    output_root = Path('agent-receipt')
    output_root.mkdir(exist_ok=True)
    (output_root / 'dispatch-envelope.json').write_text(json.dumps(envelope, indent=2) + '\n')
    with ThreadPoolExecutor(max_workers=min(3, len(bundle['tasks']))) as pool:
        futures = [pool.submit(execute, task, bundle['batch'], output_root) for task in bundle['tasks']]
        summaries = [f.result() for f in futures]
    (output_root / 'batch_summary.json').write_text(json.dumps(summaries, indent=2) + '\n')
    print(json.dumps(summaries))
    return 0 if all(s['provider_model_response_observed'] and s['failure'] is None for s in summaries) else 1


if __name__ == '__main__':
    raise SystemExit(main())
