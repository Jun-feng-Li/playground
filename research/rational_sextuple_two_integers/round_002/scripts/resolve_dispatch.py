"""Resolve source references without rewriting model outputs or controller snapshots."""
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile
import zlib


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    cache = {}
    artifacts = {}
    for item in spec['sources']:
        ref, src = item['artifact'], item['source']
        if src['kind'] == 'repo_code_block':
            text = Path(src['path']).read_text()
            matches = re.findall(r'```' + re.escape(src['language']) + r'\n(.*?)\n```', text, re.S)
            if len(matches) != 1:
                raise ValueError('Expected one original source block')
            raw = matches[0].encode()
        elif src['kind'] == 'repo_file':
            raw = Path(src['path']).read_bytes()
        elif src['kind'] == 'inline_canonical_json':
            raw = canonical(src['value'])
        elif src['kind'] in ('actions_final_answer', 'actions_member'):
            artifact_id = src['artifact_id']
            if artifact_id not in cache:
                env = dict(os.environ, GH_TOKEN=os.environ['GITHUB_TOKEN'])
                proc = subprocess.run(['gh', 'api', 'repos/Jun-feng-Li/playground/actions/artifacts/' + str(artifact_id) + '/zip'], capture_output=True, check=True, env=env, timeout=60)
                if sha(proc.stdout) != src['zip_sha256']:
                    raise ValueError('External artifact archive hash mismatch')
                cache[artifact_id] = proc.stdout
            with zipfile.ZipFile(io.BytesIO(cache[artifact_id])) as archive:
                raw = archive.read(src['member'])
            if src['kind'] == 'actions_final_answer':
                events = [json.loads(line) for line in raw.splitlines()]
                finals = [event['data']['content'] for event in events if event.get('type') == 'assistant.message' and event.get('data', {}).get('phase') == 'final_answer']
                if len(finals) != 1:
                    raise ValueError('Expected one original provider final answer')
                raw = finals[0].encode()
        else:
            raise ValueError('Unsupported source kind')
        if sha(raw) != ref['sha256'] or len(raw) != ref['size_bytes']:
            raise ValueError('Original artifact byte hash mismatch: ' + ref['object_id'])
        artifacts[ref['object_id']] = {'artifact': ref, 'content_utf8': raw.decode()}

    def resolve(value):
        if isinstance(value, dict) and '$artifact' in value:
            item = artifacts[value['$artifact']]
            result = item['content_utf8']
            if 'pointer' in value:
                result = json.loads(result)
                for key in value['pointer']:
                    result = result[key]
            return result
        if isinstance(value, dict):
            return {key: resolve(item) for key, item in value.items()}
        if isinstance(value, list):
            return [resolve(item) for item in value]
        return value

    tasks = []
    for task in spec['tasks']:
        task = resolve(task)
        card = task['card']
        if sha(canonical(card['snapshot'])) != card['input_sha256']:
            raise ValueError('Reconstructed snapshot differs from the original claimed input')
        task['submission_schema'] = card['output_schema']
        task['artifacts'] = [artifacts[ref['object_id']] for ref in card['required_reads']]
        tasks.append(task)
    bundle = {'schema': 'proofloop-independent-dispatch-batch-v1', 'batch': spec['batch'], 'tasks': tasks}
    raw = json.dumps(bundle, ensure_ascii=False, separators=(',', ':')).encode()
    envelope = {'schema': 'proofloop-dispatch-envelope-v1', 'batch': spec['batch'], 'job_ids': [t['card']['job_id'] for t in tasks], 'encoding': 'zlib-base64', 'uncompressed_size': len(raw), 'sha256': sha(raw), 'payload': base64.b64encode(zlib.compress(raw, 9)).decode()}
    dest = Path(sys.argv[2])
    dest.write_text(json.dumps(envelope, indent=2) + '\n')
    print(json.dumps({'verified_controller_snapshots': len(tasks), 'verified_artifacts': len(artifacts), 'expanded_bundle_sha256': sha(raw)}))


if __name__ == '__main__':
    main()
