import sqlite3
from pathlib import Path
from contextlib import contextmanager
DB_PATH=Path(__file__).resolve().parent.parent/'uderp.db'
SCHEMA='''
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS organizations(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,organization_id INTEGER NOT NULL,name TEXT NOT NULL,role TEXT NOT NULL,FOREIGN KEY(organization_id) REFERENCES organizations(id));
CREATE TABLE IF NOT EXISTS programmes(id INTEGER PRIMARY KEY AUTOINCREMENT,organization_id INTEGER NOT NULL,name TEXT NOT NULL,start_date TEXT,end_date TEXT,status TEXT NOT NULL DEFAULT 'ACTIVE',FOREIGN KEY(organization_id) REFERENCES organizations(id));
CREATE TABLE IF NOT EXISTS entities(id INTEGER PRIMARY KEY AUTOINCREMENT,programme_id INTEGER NOT NULL,external_id TEXT NOT NULL,entity_type TEXT NOT NULL,name TEXT NOT NULL,metadata TEXT NOT NULL DEFAULT '{}',UNIQUE(programme_id,external_id),FOREIGN KEY(programme_id) REFERENCES programmes(id));
CREATE TABLE IF NOT EXISTS documents(id INTEGER PRIMARY KEY AUTOINCREMENT,programme_id INTEGER NOT NULL,filename TEXT NOT NULL,document_type TEXT NOT NULL,content TEXT NOT NULL,uploaded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(programme_id) REFERENCES programmes(id));
CREATE TABLE IF NOT EXISTS evidence(id INTEGER PRIMARY KEY AUTOINCREMENT,document_id INTEGER NOT NULL,locator TEXT NOT NULL,excerpt TEXT NOT NULL,extraction_confidence REAL NOT NULL DEFAULT 1,FOREIGN KEY(document_id) REFERENCES documents(id));
CREATE TABLE IF NOT EXISTS facts(id INTEGER PRIMARY KEY AUTOINCREMENT,programme_id INTEGER NOT NULL,entity_id INTEGER NOT NULL,predicate TEXT NOT NULL,value_text TEXT NOT NULL,unit TEXT,period_end TEXT,evidence_id INTEGER NOT NULL,confidence REAL NOT NULL DEFAULT 1,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(programme_id) REFERENCES programmes(id),FOREIGN KEY(entity_id) REFERENCES entities(id),FOREIGN KEY(evidence_id) REFERENCES evidence(id));
CREATE TABLE IF NOT EXISTS relationships(id INTEGER PRIMARY KEY AUTOINCREMENT,programme_id INTEGER NOT NULL,source_entity_id INTEGER NOT NULL,relationship_type TEXT NOT NULL,target_entity_id INTEGER NOT NULL,confidence REAL NOT NULL DEFAULT 1,evidence_id INTEGER,FOREIGN KEY(programme_id) REFERENCES programmes(id),FOREIGN KEY(source_entity_id) REFERENCES entities(id),FOREIGN KEY(target_entity_id) REFERENCES entities(id),FOREIGN KEY(evidence_id) REFERENCES evidence(id));
CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,programme_id INTEGER NOT NULL,entity_id INTEGER,event_type TEXT NOT NULL,event_date TEXT NOT NULL,description TEXT NOT NULL,evidence_id INTEGER,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS signals(id INTEGER PRIMARY KEY AUTOINCREMENT,programme_id INTEGER NOT NULL,signal_key TEXT NOT NULL,signal_type TEXT NOT NULL,severity TEXT NOT NULL,title TEXT NOT NULL,description TEXT NOT NULL,confidence REAL NOT NULL,status TEXT NOT NULL DEFAULT 'OPEN',cluster_key TEXT,detected_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,UNIQUE(programme_id,signal_key));
CREATE TABLE IF NOT EXISTS signal_evidence(signal_id INTEGER NOT NULL,evidence_id INTEGER NOT NULL,PRIMARY KEY(signal_id,evidence_id));
CREATE TABLE IF NOT EXISTS actions(id INTEGER PRIMARY KEY AUTOINCREMENT,signal_id INTEGER NOT NULL,owner_user_id INTEGER,description TEXT NOT NULL,due_date TEXT,status TEXT NOT NULL DEFAULT 'OPEN',created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,completed_at TEXT);
CREATE TABLE IF NOT EXISTS audit_log(id INTEGER PRIMARY KEY AUTOINCREMENT,programme_id INTEGER NOT NULL,actor TEXT NOT NULL,event TEXT NOT NULL,details TEXT NOT NULL,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
'''
@contextmanager
def connect():
 c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON')
 try: yield c; c.commit()
 finally: c.close()
def init_db():
 with connect() as c: c.executescript(SCHEMA)
def reset_db():
 with connect() as c:
  for t in ['audit_log','actions','signal_evidence','signals','events','relationships','facts','evidence','documents','entities','users','programmes','organizations']:
   c.execute(f'DROP TABLE IF EXISTS {t}')
  c.executescript(SCHEMA)
