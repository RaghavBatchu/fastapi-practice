from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Products
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

# Enable CORS so the React frontend at localhost:3000 can call the API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def greet():
    return {"message": "Hello, World!"}

products = [
    Products(id=1, name="Laptop", price=999.99, description="A high-performance laptop", quantity=10),
    Products(id=2, name="Smartphone", price=499.99, description="A latest model smartphone", quantity=25),
    Products(id=3, name="Headphones", price=199.99, description="Noise-cancelling headphones", quantity=15),
    Products(id=4, name="Monitor", price=299.99, description="4K UHD Monitor", quantity=8)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    # Add initial products to the database if needed
    count = db.query(database_models.Products).count()
    if count ==0:
        for product in products:
            db.add(database_models.Products(**product.model_dump()))

    db.commit()
init_db()

@app.get("/products", response_model=List[Products])
def get_all_products(db: Session = Depends(get_db)):
    # fetch from DB then convert ORM objects to Pydantic models for JSON
    db_products = db.query(database_models.Products).all()
    result = [Products(id=p.id, name=p.name, price=p.price, description=p.description, quantity=p.quantity)
              for p in db_products]
    return result

@app.get("/product/{product_id}", response_model=Products)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Products(id=db_product.id, name=db_product.name, price=db_product.price, description=db_product.description, quantity=db_product.quantity)

@app.post("/product", response_model=Products)
def add_product(product: Products, db: Session = Depends(get_db)):
    db_product = database_models.Products(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return Products(id=db_product.id, name=db_product.name, price=db_product.price, description=db_product.description, quantity=db_product.quantity)

# Compatibility routes used by the React frontend (uses /products/ paths)
@app.post("/products", response_model=Products)
def add_product_alias(product: Products, db: Session = Depends(get_db)):
    return add_product(product=product, db=db)
    
@app.put("/product/{product_id}", response_model=Products)
def update_product(product_id: int, product: Products, db: Session = Depends(get_db)):
    p = db.query(database_models.Products).filter(database_models.Products.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    p.name = product.name
    p.price = product.price
    p.description = product.description
    p.quantity = product.quantity
    db.commit()
    db.refresh(p)
    return Products(id=p.id, name=p.name, price=p.price, description=p.description, quantity=p.quantity)

@app.put("/products/{product_id}", response_model=Products)
def update_product_alias(product_id: int, product: Products, db: Session = Depends(get_db)):
    return update_product(product_id=product_id, product=product, db=db)

@app.delete("/product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    p = db.query(database_models.Products).filter(database_models.Products.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(p)
    db.commit()
    return {"detail": "Product deleted successfully"}

@app.delete("/products/{product_id}")
def delete_product_alias(product_id: int, db: Session = Depends(get_db)):
    return delete_product(product_id=product_id, db=db)
