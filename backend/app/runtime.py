import json
from .db import connect,init_db

def seed():
 init_db()
 with connect() as c:
  if c.execute('SELECT COUNT(*) n FROM organizations').fetchone()['n']: return
  c.execute('INSERT INTO organizations(name) VALUES (?)',('UDERP Test Organization',)); org=c.execute('SELECT last_insert_rowid() id').fetchone()['id']
  for n,r in [('Programme Director','DIRECTOR'),('M&E Lead','ME'),('Finance Lead','FINANCE'),('Ministry Data Lead','DATA')]: c.execute('INSERT INTO users(organization_id,name,role) VALUES (?,?,?)',(org,n,r))
  c.execute('INSERT INTO programmes(organization_id,name,start_date,end_date) VALUES (?,?,?,?)',(org,'Uganda District Economic Resilience Programme','2026-01-01','2028-12-31')); pid=c.execute('SELECT last_insert_rowid() id').fetchone()['id']
  acts=[('A01','District market facilities'),('A02','SME grants'),('A03','Digital registry'),('A04','Vocational training'),('A05','Local infrastructure'),('A06','Women enterprise programme'),('A07','District data integration'),('A08','Market-linkage events'),('A09','Monitoring verification'),('A10','Programme evaluation')]
  meta={'A01':{'target':100,'unit':'facilities','deadline':'2026-07-31'},'A02':{'target':500,'unit':'firms','deadline':'2026-09-30','budget':2000000},'A03':{'target':20000,'unit':'beneficiaries','deadline':'2026-08-31','depends_on':['A07']},'A04':{'target':1200,'unit':'youth','deadline':'2026-12-31'},'A05':{'target':40,'unit':'sites','deadline':'2026-10-31'},'A06':{'target':800,'unit':'women','deadline':'2026-11-30'},'A07':{'target':10,'unit':'districts','deadline':'2026-07-31'},'A08':{'target':30,'unit':'events','deadline':'2026-09-30','depends_on':['A01']},'A09':{'target':10,'unit':'districts','deadline':'2026-09-30'},'A10':{'target':1,'unit':'evaluation','deadline':'2026-12-31','depends_on':['A09']}}
  for eid,name in acts: c.execute('INSERT INTO entities(programme_id,external_id,entity_type,name,metadata) VALUES (?,?,?,?,?)',(pid,eid,'ACTIVITY',name,json.dumps(meta[eid])))
  a01=c.execute("SELECT id FROM entities WHERE external_id='A01'").fetchone()['id']; c.execute('INSERT INTO events(programme_id,entity_id,event_type,event_date,description) VALUES (?,?,?,?,?)',(pid,a01,'DEADLINE_CHANGED','2026-07-10','Original deadline changed to 2026-07-31.'))
  c.execute('INSERT INTO audit_log(programme_id,actor,event,details) VALUES (?,?,?,?)',(pid,'system','PROGRAMME_CREATED','Seeded hostile UDERP programme'))
  for src,tgt in [('A03','A07'),('A08','A01'),('A10','A09')]:
   s=c.execute('SELECT id FROM entities WHERE external_id=?',(src,)).fetchone()['id']; t=c.execute('SELECT id FROM entities WHERE external_id=?',(tgt,)).fetchone()['id']; c.execute('INSERT INTO relationships(programme_id,source_entity_id,relationship_type,target_entity_id) VALUES (?,?,?,?)',(pid,s,'DEPENDS_ON',t))
  return pid
