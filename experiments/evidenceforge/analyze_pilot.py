"""Independent format, provenance and bounded-scenario checks (not the DSL engine)."""
from pathlib import Path
from datetime import datetime
from collections import Counter
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inspect(name):
    base = ROOT/name
    manifest = json.loads((base/'GENERATION_MANIFEST.json').read_text(encoding='utf-8'))
    records = Counter(); json_errors=[]; failures=[]; successes=[]; connections=[]; ids=[]
    for path in sorted((base/'data').rglob('*')):
        if not path.is_file():continue
        lines=path.read_text(encoding='utf-8').splitlines()
        records[str(path.relative_to(base))]=len(lines)
        if path.suffix=='.json':
            for i,line in enumerate(lines,1):
                try:
                    obj=json.loads(line)
                    if path.name=='conn.json': connections.append(obj)
                except json.JSONDecodeError:json_errors.append([str(path),i])
        if path.name=='syslog.log':
            for line in lines:
                stamp=re.search(r'^<\d+>1 (\S+)',line)
                if not stamp:continue
                t=datetime.fromisoformat(stamp[1].replace('Z','+00:00'))
                m=re.search(r'Failed password for (?:invalid user )?(\S+) from (\S+) port (\d+)',line)
                if m:failures.append({'time':t.isoformat(),'username':m[1],'src_ip':m[2],'src_port':int(m[3])})
                m=re.search(r'Accepted (?:password|publickey) for (\S+) from (\S+) port (\d+)',line)
                if m:successes.append({'time':t.isoformat(),'username':m[1],'src_ip':m[2],'src_port':int(m[3])})
        if path.name=='snort_alert.log':ids.extend(lines)
    attack=sorted(datetime.fromisoformat(x['time']) for x in failures if x['src_ip']=='203.0.113.50')
    max60=max((sum(0<=(t-v).total_seconds()<60 for v in attack) for t in attack),default=0)
    ports=sorted({x['id.resp_p'] for x in connections if x.get('id.orig_h')=='10.77.0.10'
                  and x.get('id.resp_h')=='10.77.0.20' and 8000<=x.get('id.resp_p',0)<=8019})
    scan_targets={}
    for x in connections:
        if x.get('id.orig_h')=='10.77.0.10' and 8000<=x.get('id.resp_p',0)<=8019:
            scan_targets.setdefault(x['id.resp_h'],set()).add(x['id.resp_p'])
    verified=all(sha(base/p)==digest for p,digest in manifest['files'].items())
    return {'bundle':name,'version':manifest['evidenceforge_version'],'seed':manifest['generation_seed'],
        'records_by_file':dict(records),'data_file_count':len(records),'total_data_lines':sum(records.values()),
        'ndjson_errors':json_errors,'manifest_hashes_match':verified,
        'attack_failed_password_records':len(attack),'attack_failures_max_60s':max60,
        'attack_success_records':sum(x['src_ip']=='203.0.113.50' for x in successes),
        'benign_failed_password_records':sum(x['src_ip']=='10.77.0.10' for x in failures),
        'scan_distinct_target_ports':len(ports),'scan_ports':ports,
        'scan_ports_by_observed_target':{k:len(v) for k,v in scan_targets.items()},
        'matching_auth_and_ids':any('203.0.113.50:' in s and '10.77.0.20:22' in s for s in ids),
        'eve_json_files':len(list((base/'data').rglob('eve*.json'))),
        'failures':failures,'successes':successes}

for required in ['run-native-a', 'run-native-b', 'run-bulk-a']:
    if not (ROOT/required/'GENERATION_MANIFEST.json').is_file() or not (ROOT/required/'data').is_dir():
        raise SystemExit(f'Missing generated bundle: {required}. Follow README generation steps first.')

results={name:inspect(name) for name in ['run-native-a','run-native-b','run-bulk-a'] if (ROOT/name/'GENERATION_MANIFEST.json').exists()}
a,b=ROOT/'run-native-a'/'data',ROOT/'run-native-b'/'data'
files_a={str(p.relative_to(a)):sha(p) for p in a.rglob('*') if p.is_file()}
files_b={str(p.relative_to(b)):sha(p) for p in b.rglob('*') if p.is_file()}
result={'source_commit':'79fcfcdf3726168dacfede5a27aab2aa7a2f3d69',
        'study_date':'2026-10-28','original_scenario_repeat_data_identical':files_a==files_b,
        'comparison_scope':'Only emitted data files; wall-clock generation metadata excluded.',
        'runs':results,
        'limitations':['Reference record inspection, not a test of the future DSL motor.',
            'Fast-format IDS and Zeek conn are not Suricata EVE alert/flow.',
            'Generator acceptance must be read from evaluation report, not process exit code.']}
(ROOT/'analysis_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
for name,run in results.items():
    print(name,json.dumps({k:v for k,v in run.items() if k not in ['records_by_file','failures','successes','scan_ports']},ensure_ascii=False))
print('repeat_data_identical:',files_a==files_b)
