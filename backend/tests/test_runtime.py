from app.db import reset_db,connect
from app.runtime import seed

def setup_function(): reset_db(); seed()
def test_persistent_runtime_has_org_graph_and_history():
 with connect() as c:
  assert c.execute('SELECT COUNT(*) n FROM organizations').fetchone()['n']==1
  assert c.execute('SELECT COUNT(*) n FROM entities').fetchone()['n']==10
  assert c.execute('SELECT COUNT(*) n FROM events').fetchone()['n']>=1
  assert c.execute('SELECT COUNT(*) n FROM relationships').fetchone()['n']==3
