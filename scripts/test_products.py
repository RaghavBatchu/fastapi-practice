import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import main
from database import session

# Create a real DB session and pass it to the endpoint function (mimics FastAPI DI)
db = session()
try:
    res = main.get_all_products(db=db)
    print('RETURNED_TYPE:', type(res))
    print('RETURNED_REPR:', repr(res))

    # If it's a list of Pydantic-like objects or SQLAlchemy objects, show a simple summary
    if isinstance(res, list):
        print('LENGTH:', len(res))
        if len(res) > 0:
            print('FIRST_ITEM_TYPE:', type(res[0]))
            # If SQLAlchemy object, print its __dict__ keys
            try:
                print('FIRST_ITEM_DIR_KEYS:', list(res[0].__dict__.keys()))
            except Exception:
                pass
except Exception as e:
    print('CALL_ERROR:')
    import traceback
    traceback.print_exc()
finally:
    db.close()
