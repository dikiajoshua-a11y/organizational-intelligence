from datetime import date
from .db import connect
TODAY=date(2026,9,8)
def _meta(c,p,e): import json; return json.loads(c.execute('SELECT metadata FROM entities WHERE programme_id=? AND external_id=?',(p,e)).fetchone()['metadata'])
def _fact(c,p,e,pred): return c.execute('''SELECT f.* FROM facts f JOIN entities e ON e.id=f.entity_id WHERE f.programme_id=? AND e.external_id=? AND f.predicate=? ORDER BY f.id DESC LIMIT 1''',(p,e,pred)).fetchone()
def recompute(p):
 with connect() as c:
  c.execute('DELETE FROM signal_evidence WHERE signal_id IN (SELECT id FROM signals WHERE programme_id=?)',(p,)); c.execute('DELETE FROM actions WHERE signal_id IN (SELECT id FROM signals WHERE programme_id=?)',(p,)); c.execute('DELETE FROM signals WHERE programme_id=?',(p,))
  out=[]
  def add(k,t,s,title,desc,conf,cluster,action,ev=[]):
   c.execute('INSERT INTO signals(programme_id,signal_key,signal_type,severity,title,description,confidence,cluster_key) VALUES (?,?,?,?,?,?,?,?)',(p,k,t,s,title,desc,conf,cluster)); sid=c.execute('SELECT last_insert_rowid() id').fetchone()['id']
   for e in ev: c.execute('INSERT OR IGNORE INTO signal_evidence(signal_id,evidence_id) VALUES (?,?)',(sid,e))
   c.execute('INSERT INTO actions(signal_id,description) VALUES (?,?)',(sid,action)); out.append(k)
  m=_meta(c,p,'A07'); f=_fact(c,p,'A07','completion')
  if f and TODAY.isoformat()>m['deadline'] and float(f['value_text'])<m['target']: add('A07_OVERDUE','DEVIATION','CRITICAL','District integration is overdue',f"{f['value_text']}/{m['target']} {m['unit']} integrated against {m['deadline']}.",.98,'CLUSTER-A07-A03','Complete remaining integrations and update the delivery plan.',[f['evidence_id']])
  m=_meta(c,p,'A03'); f=_fact(c,p,'A03','completion')
  if f and float(f['value_text'])<m['target']: add('A03_DEPENDENCY','DEPENDENCY_RISK','HIGH','Beneficiary registration is exposed',f"A03 is at {f['value_text']}/{m['target']} while dependency A07 is overdue.",.94,'CLUSTER-A07-A03','Resolve A07 and reassess A03.',[f['evidence_id']])
  m=_meta(c,p,'A02'); exp=_fact(c,p,'A02','expenditure')
  if exp and float(exp['value_text'])>m['budget']: add('A02_RESOURCE','RESOURCE_VARIANCE','CRITICAL','Beta funding position requires reconciliation',f"Reported expenditure is ${float(exp['value_text']):,.0f} against a ${m['budget']:,.0f} approved baseline.",.90,'CLUSTER-A02-FUNDING','Finance and Secretariat should reconcile expenditure against the latest authorization.',[exp['evidence_id']])
  due=_fact(c,p,'A07','commitment_due'); done=_fact(c,p,'A07','commitment_completion_evidence')
  if due and done and TODAY.isoformat()>due['value_text'] and done['value_text']=='NOT_FOUND': add('A07_COMMITMENT','OVERDUE_COMMITMENT','CRITICAL','Ministry data commitment is overdue',f"Dataset was due {due['value_text']}; completion evidence was not identified.",.96,'CLUSTER-A07-A03','Ministry data lead should provide or formally update the commitment status.',[due['evidence_id'],done['evidence_id']])
  return len(out)
def state(p):
 with connect() as c: return [dict(r) for r in c.execute("SELECT * FROM signals WHERE programme_id=? AND status='OPEN' ORDER BY CASE severity WHEN 'CRITICAL' THEN 4 WHEN 'HIGH' THEN 3 WHEN 'MEDIUM' THEN 2 ELSE 1 END DESC,confidence DESC",(p,)).fetchall()]