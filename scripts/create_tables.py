import sys
import os
import traceback

# ensure project root (parent of this scripts folder) is on sys.path so imports
# like `import database_models` work when running this file directly
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import database_models
import database

try:
    database_models.Base.metadata.create_all(bind=database.engine)
    print("CREATE_ALL_DONE")
except Exception:
    print("CREATE_ALL_FAILED")
    traceback.print_exc()
    sys.exit(1)
