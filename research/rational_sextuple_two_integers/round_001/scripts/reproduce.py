"""Reproduce the bounded experiment; verify its mathematical-content fingerprint.
All operations are local. This driver does not invoke AI agents or ProofLoop.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time

def graph_fingerprint(results):
 entries=[]
 for p in sorted(results.glob('anchors_H*/anchor_*.json')):
  value=json.loads(p.read_text());value.pop('elapsed_seconds',None)
  digest=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  entries.append(str(p.relative_to(results))+'\0'+digest)
 return hashlib.sha256('\n'.join(entries).encode()).hexdigest(),len(entries)

def main(workspace,workers):
 root=workspace.resolve();results=root/'results';results.mkdir(parents=True,exist_ok=True)
 scripts=Path(__file__).resolve().parent;start=time.monotonic();commands=[]
 def run(name,*args):
  cmd=[sys.executable,'-B',str(scripts/name),*map(str,args)]
  subprocess.run(cmd,check=True);commands.append({'script':name,'arguments':list(map(str,args)),'exit_code':0})
 run('anchor_search.py','--height',48,'--anchor-max',50,'--workers',workers,'--output',results/'anchors_H48')
 run('anchor_search.py','--height',96,'--selected','--workers',workers,'--output',results/'anchors_H96')
 run('family_search.py','--height',60,'--output',results/'family_search_H60.json')
 run('audit_graphs.py','--results',results,'--workers',workers,'--output',results/'crosscheck.json')
 run('quadruple_route.py','--results',results,'--output',results/'quadruple_route.json')
 run('quintuple_extensions.py','--results',results,'--output',results/'quintuple_extensions.json')
 run('checks.py','--output',results/'regression_reproduced.json')
 fingerprint,count=graph_fingerprint(results)
 expected=json.loads((root/'expected_results.json').read_text())
 assert count==expected['graphs'] and fingerprint==expected['canonical_graph_collection_sha256']
 cross=json.loads((results/'crosscheck.json').read_text())
 assert cross['all_pass'] and cross['total_pair_checks']==expected['pair_tests_per_implementation']
 q=json.loads((results/'quintuple_extensions.json').read_text())
 assert q['distinct_input_quintuples']==2328 and q['nonzero_new_candidates_checked']==102917 and not q['sextuple_witnesses']
 f=json.loads((results/'family_search_H60.json').read_text())
 assert sum(x['valid_sextuples_verified'] for x in f['rows'])==6604 and not f['integer_hits'] and not f['arithmetic_failures']
 d=json.loads((results/'quadruple_route.json').read_text())
 assert d['pairing_conditions_tested']==339135 and len(d['condition_hits'])==4 and not d['sextuple_candidates']
 receipt={'schema':'reproduction-receipt-v1','python':sys.version,'all_pass':True,'graphs':count,
 'canonical_graph_collection_sha256':fingerprint,'pair_tests_per_implementation':cross['total_pair_checks'],
 'commands':commands,'elapsed_seconds':round(time.monotonic()-start,3),
 'native_proofloop_executed':False,'independent_ai_agents':0,'main_goal_status':'unresolved'}
 (results/'reproduction_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--workspace',type=Path,default=Path(__file__).resolve().parent.parent);p.add_argument('--workers',type=int,default=4);a=p.parse_args();main(a.workspace,a.workers)
