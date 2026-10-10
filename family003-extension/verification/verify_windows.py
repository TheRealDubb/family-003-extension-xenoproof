"""Native Windows statement/axiom checks, full Lean replay, quotient postcheck.

Requires the pinned lean4export and the supplied OfflineReplay adapter built
against the pinned Comparator. Does not provide a production sandbox.
Run with --help for parameters. Sources are never generated or changed.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,subprocess,sys,time
PRIMITIVES='Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight String.ofList Char.ofNat List eagerReduce Nat String String.mk Char optParam autoParam semiOutParam outParam'.split()
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['project','exporter','driver','output']:parser.add_argument('--'+name,required=True,type=Path)
    args=parser.parse_args();project=args.project.resolve();output=args.output.resolve()
    output.mkdir(parents=True,exist_ok=False)
    config=project/'ComparatorChallenges/FrontierTightPublicBoundary.json'
    cfg=json.loads(config.read_text());receipt={'scope':'Native Windows development mode; no Linux sandbox or independent kernel.',
       'config_sha256':sha(config),'exporter_sha256':sha(args.exporter),'driver_sha256':sha(args.driver),
       'permitted_axioms':cfg['permitted_axioms'],'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'theorem_names':cfg['theorem_names'],'exports':{}}
    assert set(cfg['permitted_axioms'])=={'propext','Classical.choice','Quot.sound'}
    env=os.environ.copy()
    # Read Lake's reported assignments directly. The tested Windows Lake child
    # launch omitted LEAN_PATH, although `lake env` reported the correct paths.
    # These remain Lake-generated paths from THIS checkout, not a custom map.
    capture=subprocess.run(['lake','env'],cwd=project,env=env,text=True,
       encoding='utf-8',capture_output=True)
    assert capture.returncode==0,capture.stderr
    reported=dict(line.split('=',1) for line in capture.stdout.splitlines() if '=' in line)
    for key in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LEAN_GITHASH','PATH']:
        if key in reported:env[key]=reported[key]
    assert env.get('LEAN_PATH'),'Lake did not report a library search path'
    path_entries=env['LEAN_PATH'].split(os.pathsep)
    resolved_paths=[]
    for entry in path_entries:
        p=Path(entry);p=(project/p).resolve() if not p.is_absolute() else p.resolve()
        resolved_paths.append(p)
        # Runtime stdlib may sit outside project; all package/project paths must be local.
        if '.lake' in p.parts:assert p.is_relative_to(project),str(p)
    assert (project/'.lake/build/lib/lean').resolve() in resolved_paths
    receipt['all_package_search_paths_in_test_checkout']=True
    receipt['search_path_source']='Lake env reported assignments from the test checkout'
    receipt['search_path_entry_count']=len(path_entries)
    extras=['propext','Quot.sound','Classical.choice','Quot','Quot.mk','Quot.lift','Quot.ind']+PRIMITIVES
    def save():
        (output/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
    for side in ['challenge','solution']:
        module=cfg[side+'_module'];rel=Path(*module.split('.'))
        src=project/rel.with_suffix('.lean');obj=project/'.lake/build/lib/lean'/rel.with_suffix('.olean')
        binding={'source_sha256':sha(src),'olean_sha256':sha(obj)}
        stream=output/(side+'.ndjson');err=output/(side+'.stderr');started=time.time()
        print('Exporting '+side,flush=True)
        with stream.open('wb') as out,err.open('wb') as log:
            p=subprocess.run([str(args.exporter.resolve()),module,'--',*cfg['theorem_names'],*cfg.get('definition_names',[]),*extras],
              cwd=project,env=env,stdout=out,stderr=log)
        receipt['exports'][side]={'module':module,'exit_code':p.returncode,'seconds':time.time()-started,
             **binding,'stream_sha256':sha(stream),'bytes':stream.stat().st_size,'stderr_sha256':sha(err)};save()
        assert p.returncode==0,err.read_text(errors='replace')
        assert sha(src)==binding['source_sha256'] and sha(obj)==binding['olean_sha256']
    log=output/'replay.log';started=time.time();print('Statement comparison, axiom audit and full dependency kernel replay',flush=True)
    with log.open('wb') as out:
        p=subprocess.run([str(args.driver.resolve()),str(config),str(output/'challenge.ndjson'),str(output/'solution.ndjson')],
             cwd=project,env=env,stdout=out,stderr=subprocess.STDOUT)
    result=log.read_text(encoding='utf-8',errors='replace')
    markers=['STATEMENT_COMPARISON_PASSED','AXIOM_AUDIT_PASSED','KERNEL_REPLAY_AND_QUOTIENT_POSTCHECK_PASSED','OFFLINE_REPLAY_PASSED']
    receipt['replay']={'exit_code':p.returncode,'seconds':time.time()-started,'output':result,'log_sha256':sha(log)}
    receipt['passed']=p.returncode==0 and all(m in result for m in markers)
    receipt['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()
    assert receipt['passed'],result
    print(result,flush=True)
if __name__=='__main__':main()
