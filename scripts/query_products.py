import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from database import session
import database_models

if __name__ == '__main__':
    db = session()
    try:
        rows = db.query(database_models.Products).all()
        print('ROW_COUNT:', len(rows))
        for r in rows:
            print(f'id={r.id} name={r.name!r} price={r.price} description={r.description!r} quantity={r.quantity}')
    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        db.close()
