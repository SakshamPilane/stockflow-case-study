# models.py
# Minimal placeholder SQLAlchemy models used only for import resolution. These are NOT full implementations.
from app import db

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sku = db.Column(db.String)
    price = db.Column(db.Numeric)
    product_type_id = db.Column(db.Integer)
    low_stock_threshold = db.Column(db.Integer)

class Warehouse(db.Model):
    __tablename__ = "warehouses"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    name = db.Column(db.String)

class Inventory(db.Model):
    __tablename__ = "inventories"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    warehouse_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

class Supplier(db.Model):
    __tablename__ = "suppliers"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    name = db.Column(db.String)
    contact_email = db.Column(db.String)

class SupplierProduct(db.Model):
    __tablename__ = "supplier_products"
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    lead_time_days = db.Column(db.Integer)

class Sale(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    warehouse_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
