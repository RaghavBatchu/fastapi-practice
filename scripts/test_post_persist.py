import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from database import session
import main
from models import Products
import database_models

# create a test product with a (hopefully) unused id
test_id = 9999
p = Products(id=test_id, name="TEST_PRODUCT", price=1.23, description="created by test", quantity=1)

db = session()
try:
    # ensure doesn't already exist
    existing = db.query(database_models.Products).filter(database_models.Products.id == test_id).first()
    if existing:
        print('TEST_ID_ALREADY_EXISTS')
    else:
        added = main.add_product(product=p, db=db)
        print('ADD_RETURNED:', added)
        # verify in DB
        found = db.query(database_models.Products).filter(database_models.Products.id == test_id).first()
        if found:
            print('PERSISTED: id=', found.id, 'name=', found.name)
        else:
            print('NOT_PERSISTED')
finally:
    db.close()
