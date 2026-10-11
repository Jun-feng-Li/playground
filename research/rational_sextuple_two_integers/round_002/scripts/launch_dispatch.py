"""Public transport loader; original ProofLoop controller remains authoritative."""
from pathlib import Path
import base64, hashlib, importlib.util, json, lzma, subprocess, sys, zlib

ROOT = Path.cwd().resolve()
BASE = 'research/rational_sextuple_two_integers/round_002/'

def digest(b):
    return hashlib.sha256(b).hexdigest()

def canonical(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()

def read_relative(name, expected=None):
    p = (ROOT / name).resolve()
    if ROOT not in p.parents:
        raise ValueError('Transport source escapes repository')
    raw = p.read_bytes()
    if expected and digest(raw) != expected:
        raise ValueError('Transport source digest mismatch: ' + name)
    return raw

def expand(envelope):
    if envelope['encoding'] in ('zlib-base64', 'lzma-base64'):
        f = zlib.decompress if envelope['encoding'] == 'zlib-base64' else lzma.decompress
        raw = f(base64.b64decode(envelope['payload']))
        if len(raw) != envelope['uncompressed_size'] or digest(raw) != envelope['sha256']:
            raise ValueError('Frozen bundle digest mismatch')
        return json.loads(raw)
    if envelope['encoding'] != 'reference-batch-v1':
        raise ValueError('Unsupported transport format')
    prior = json.loads(read_relative(envelope['base_dispatch'], envelope['base_dispatch_sha256']))
    bundle = expand(prior)
    wanted = set(envelope['job_ids'])
    bundle['tasks'] = [t for t in bundle['tasks'] if t['card']['job_id'] in wanted]
    bundle['batch'] = envelope['batch']
    for task in bundle['tasks']:
        job = task['card']['job_id']
        repair = envelope['repairs'][job]
        old = read_relative(repair['previous_output_path'], repair['previous_output_sha256']).decode('utf-8')
        task['delivery_feedback'] = {'previous_unaccepted_output': old, 'native_controller_error': repair['controller_error'], 'instruction': envelope['repair_instruction']}
    raw = canonical(bundle)
    if len(raw) != envelope['uncompressed_size'] or digest(raw) != envelope['sha256']:
        raise ValueError('Expanded reference bundle differs from frozen host bundle')
    return bundle

def main():
    changed = subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','HEAD'], text=True).splitlines()
    selected = [p for p in changed if p.startswith(BASE+'recovery_001/dispatch/') and p.endswith('.json')]
    if len(selected) != 1:
        raise ValueError('Expected one newly committed dispatch, not an automatic replay')
    original = read_relative(selected[0])
    envelope = json.loads(original)
    bundle = expand(envelope)
    if [t['card']['job_id'] for t in bundle['tasks']] != envelope['job_ids']:
        raise ValueError('Task identities changed during transport')
    for task in bundle['tasks']:
        for item in task.pop('artifact_paths', []):
            text = read_relative(item['path'], item['artifact']['sha256']).decode('utf-8')
            task['artifacts'].append({'artifact':item['artifact'], 'content_utf8':text})
    output = ROOT/'agent-receipt'
    output.mkdir(exist_ok=True)
    (output/'source-dispatch.json').write_bytes(original)
    raw = canonical(bundle)
    target = output/'expanded-dispatch.json'
    target.write_bytes(canonical({'batch':bundle['batch'], 'job_ids':envelope['job_ids'], 'encoding':'zlib-base64', 'payload':base64.b64encode(zlib.compress(raw,9)).decode(), 'uncompressed_size':len(raw), 'sha256':digest(raw)}))
    runner = ROOT/BASE/'scripts/run_independent_batch.py'
    spec = importlib.util.spec_from_file_location('transport', runner)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.argv = [str(runner), str(target)]
    return module.main()

if __name__ == '__main__':
    raise SystemExit(main())
