"""Lossless public transport; the unchanged native controller is authoritative."""
from pathlib import Path
import base64, hashlib, importlib.util, json, lzma, subprocess, sys, zlib
ROOT = Path.cwd().resolve()
BASE = 'research/rational_sextuple_two_integers/round_002/'
CACHE = {}

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

def resolve(value):
    if isinstance(value, dict) and set(value) == {'_transport_ref'}:
        r = value['_transport_ref']
        key = (r['path'], r['sha256'], r['kind'])
        if key not in CACHE:
            raw = read_relative(r['path'], r['sha256'])
            obj = json.loads(raw)
            if r['kind'] == 'dispatch':
                obj = expand(obj)
            elif r['kind'] != 'json':
                raise ValueError('Invalid reference kind')
            CACHE[key] = obj
        obj = CACHE[key]
        pointer = r['pointer']
        if pointer:
            if not pointer.startswith('/'):
                raise ValueError('Invalid JSON pointer')
            for part in pointer[1:].split('/'):
                part = part.replace('~1', '/').replace('~0', '~')
                obj = obj[int(part)] if isinstance(obj, list) else obj[part]
        return json.loads(canonical(obj))
    if isinstance(value, dict):
        return {k:resolve(v) for k,v in value.items()}
    if isinstance(value, list):
        return [resolve(v) for v in value]
    return value

def expand(envelope):
    encoding = envelope['encoding']
    if encoding in ('zlib-base64', 'lzma-base64'):
        f = zlib.decompress if encoding == 'zlib-base64' else lzma.decompress
        raw = f(base64.b64decode(envelope['payload']))
        if len(raw) != envelope['uncompressed_size'] or digest(raw) != envelope['sha256']:
            raise ValueError('Frozen bundle digest mismatch')
        return json.loads(raw)
    if encoding == 'template-lzma-base64':
        template = lzma.decompress(base64.b64decode(envelope['payload']))
        if digest(template) != envelope['template_sha256']:
            raise ValueError('Template digest mismatch')
        bundle = resolve(json.loads(template))
    elif encoding == 'object-template-v1':
        bundle = resolve(envelope['template'])
    elif encoding == 'reference-batch-v1':
        prior = json.loads(read_relative(envelope['base_dispatch'], envelope['base_dispatch_sha256']))
        bundle = expand(prior)
        wanted = set(envelope['job_ids'])
        bundle['tasks'] = [t for t in bundle['tasks'] if t['card']['job_id'] in wanted]
        bundle['batch'] = envelope['batch']
        for task in bundle['tasks']:
            repair = envelope['repairs'][task['card']['job_id']]
            old = read_relative(repair['previous_output_path'], repair['previous_output_sha256']).decode('utf-8')
            task['delivery_feedback'] = {'previous_unaccepted_output': old, 'native_controller_error': repair['controller_error'], 'instruction': envelope['repair_instruction']}
    else:
        raise ValueError('Unsupported transport format')
    raw = canonical(bundle)
    if len(raw) != envelope['uncompressed_size'] or digest(raw) != envelope['sha256']:
        raise ValueError('Expanded bundle differs from original frozen native workcards')
    return bundle

def main():
    changed = subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','HEAD'], text=True).splitlines()
    selected = [p for p in changed if p.startswith(BASE+'recovery_001/dispatch/') and p.endswith('.json')]
    if len(selected) != 1:
        raise ValueError('Expected one new dispatch, not an automatic replay')
    original = read_relative(selected[0])
    envelope = json.loads(original)
    bundle = expand(envelope)
    if [t['card']['job_id'] for t in bundle['tasks']] != envelope['job_ids']:
        raise ValueError('Task identity mismatch')
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
