"""Restore exact native SQLite table contents and original MCP messages.

The database's physical page layout need not match the source file. Logical
column types and values, and every exported MCP message byte, must match.
No model is run, no credentials are restored, and no repository is modified.
"""
from __future__ import annotations
import argparse,base64,hashlib,importlib.util,json,sqlite3
from pathlib import Path

SCHEMAS={
'metadata':['key','value'], 'runs':['run_id','state'],
'objects':['object_id','run_id','sha256','media_type','body'],
'writes':['scope','key','request_sha','result'],
'reads':['principal','run_id','object_id','sha256','next_offset'],
'deliveries':['run_id','job_id','generation','arguments','arguments_sha','received_at','status','response']}

def canonical(x):
    return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8')
def digest(b): return hashlib.sha256(b).hexdigest()
def decode_cell(c):
    if not isinstance(c,dict):return c
    if set(c)=={'blob_json'}:return canonical(c['blob_json'])
    if set(c)=={'blob_utf8'}:return c['blob_utf8'].encode('utf-8')
    if set(c)=={'blob_base64'}:return base64.b64decode(c['blob_base64'],validate=True)
    raise ValueError('Unknown typed SQLite cell')
def encode_cell(c):
    if isinstance(c,bytes):
        try:
            j=json.loads(c)
            if canonical(j)==c:return {'blob_json':j}
        except (UnicodeDecodeError,ValueError):pass
        try:return {'blob_utf8':c.decode('utf-8')}
        except UnicodeDecodeError:return {'blob_base64':base64.b64encode(c).decode('ascii')}
    return c

def restore(logical, directory):
    if logical['schema']!='proofloop-logical-checkpoint-v1':raise ValueError('Wrong checkpoint type')
    directory=Path(directory).resolve()
    if directory.exists():raise FileExistsError('Restore destination must not exist')
    state=directory/'workspace/.jules/proofloop-state';state.mkdir(parents=True)
    db=state/'proofloop.sqlite3'
    tables=logical['tables']
    if [t['name'] for t in tables]!=sorted(SCHEMAS):raise ValueError('Unexpected native tables')
    if digest(canonical(tables))!=logical['table_data_sha256']:raise ValueError('Table digest mismatch')
    with sqlite3.connect(db) as c:
        for t in tables:
            name=t['name'];cols=t['columns']
            if cols!=SCHEMAS[name]:raise ValueError('Unexpected native columns')
            if not t['schema_sql'].lstrip().upper().startswith('CREATE TABLE '+name.upper()+' ') or ';' in t['schema_sql']:
                raise ValueError('Unexpected table DDL')
            c.execute(t['schema_sql'])
            c.executemany('INSERT INTO '+name+' VALUES ('+','.join('?' for _ in cols)+')',
                          [tuple(decode_cell(x) for x in row) for row in t['rows']])
        c.commit()
        if c.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('SQLite integrity failure')
        observed=[]
        for t in tables:
            info=c.execute('PRAGMA table_info('+t['name']+')').fetchall()
            order=','.join('"'+i[1]+'"' for i in sorted(info,key=lambda i:i[5]) if i[5])
            rows=c.execute('SELECT * FROM '+t['name']+' ORDER BY '+order).fetchall()
            o=dict(t);o['rows']=[[encode_cell(x) for x in row] for row in rows];observed.append(o)
        if digest(canonical(observed))!=logical['table_data_sha256']:raise ValueError('Restored table values differ')
        for object_id,sha,body in c.execute('SELECT object_id,sha256,body FROM objects'):
            if digest(body)!=sha:raise ValueError('Original object body hash mismatch: '+object_id)
        run=json.loads(c.execute('SELECT state FROM runs WHERE run_id=?',(logical['run_id'],)).fetchone()[0])
    journal=directory/'mcp';journal.mkdir()
    for item in logical['files']:
        name=item['path']
        if not name.startswith('mcp/'):raise ValueError('Unexpected journal directory')
        name=name[4:]
        if Path(name).name!=name or not name.endswith('.json'):raise ValueError('Unsafe journal filename')
        if item['encoding']=='canonical-json-newline':raw=canonical(item['content'])+b'\n'
        elif item['encoding']=='canonical-json':raw=canonical(item['content'])
        elif item['encoding']=='utf8':raw=item['content'].encode('utf-8')
        else:raise ValueError('Unknown journal codec')
        if len(raw)!=item['size_bytes'] or digest(raw)!=item['sha256']:raise ValueError('Journal bytes differ')
        (journal/name).write_bytes(raw)
    receipt={'schema':'native-logical-restore-receipt-v1','run_id':run['run_id'],'revision':run['revision'],
             'run_status':run['run_status'],'goal_status':run['goal_status'],'phase':run['meta']['phase'],
             'tables_verified':len(tables),'objects_verified':sum(t['name']=='objects' and len(t['rows']) or 0 for t in tables),
             'journal_files_verified':len(logical['files']),'table_content_sha256':logical['table_data_sha256'],
             'sqlite_integrity':'ok','physical_sqlite_sha256':digest(db.read_bytes()),
             'source_physical_sqlite_sha256':logical['source_database_sha256'],
             'physical_layout_equality_claimed':False,'credentials_included':False,'native_controller_execution_by_this_script':False}
    (directory/'restore_receipt.json').write_bytes(canonical(receipt)+b'\n')
    (directory/'logical_checkpoint.json').write_bytes(canonical(logical)+b'\n')
    return receipt

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--logical-json');p.add_argument('--manifest');p.add_argument('--repository-root');p.add_argument('--directory',required=True);a=p.parse_args()
    if bool(a.logical_json)==bool(a.manifest):p.error('Supply exactly one of --logical-json and --manifest')
    if a.logical_json:logical=json.loads(Path(a.logical_json).read_bytes())
    else:
        root=Path(a.repository_root or '.').resolve();manifest=Path(a.manifest).resolve();e=json.loads(manifest.read_bytes());parts=[]
        for item in e['payload_parts']:
            if Path(item['path']).name!=item['path']:raise ValueError('Unsafe part path')
            raw=(manifest.parent/item['path']).read_bytes()
            if len(raw)!=item['size_bytes'] or digest(raw)!=item['sha256']:raise ValueError('Checkpoint part digest mismatch')
            parts.append(raw.decode('ascii').strip())
        e['payload']=''.join(parts)
        loader=root/'research/rational_sextuple_two_integers/round_002/scripts/launch_dispatch.py'
        spec=importlib.util.spec_from_file_location('reference_transport',loader);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.ROOT=root
        logical=m.expand(e)
    print(json.dumps(restore(logical,a.directory),ensure_ascii=False))

if __name__=='__main__':main()
