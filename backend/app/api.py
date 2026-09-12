from fastapi import FastAPI,UploadFile,File,HTTPException
from .db import connect,init_db
from .runtime import seed
from .signals import recompute,state
app=FastAPI(title='UDERP Organizational Runtime',version='1.0.0')
@app.on_event('startup')
def startup(): init_db(); seed()
@app.get('/')
def root(): return {'system':'UDERP Organizational Runtime','version':'1.0.0','principle':'organizational capabilities first'}
@app.get('/programmes/{pid}/state')
def programme_state(pid:int):
 recompute(pid)
 with connect() as c:
  p=c.execute('SELECT * FROM programmes WHERE id=?',(pid,)).fetchone()
  if not p: raise HTTPException(404,'Programme not found')
  return {'programme':dict(p),'signals':state(pid)}
@app.get('/programmes/{pid}/timeline')
def timeline(pid:int):
 with connect() as c: return [dict(r) for r in c.execute('SELECT * FROM events WHERE programme_id=? ORDER BY event_date,id',(pid,)).fetchall()]
@app.get('/programmes/{pid}/actions')
def actions(pid:int):
 with connect() as c: return [dict(r) for r in c.execute('SELECT a.*,s.title signal_title FROM actions a JOIN signals s ON s.id=a.signal_id WHERE s.programme_id=? ORDER BY a.status,a.id',(pid,)).fetchall()]
