# part1_fixed_create_product.py
from decimal import Decimal, InvalidOperation
from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
from app import db
from models import Product, Inventory, Warehouse
from sqlalchemy import select

app = Flask(__name__)

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json() or {}
    name = data.get('name')
    sku = data.get('sku')
    price_raw = data.get('price')
    warehouses = data.get('warehouses')
    if not warehouses and data.get('warehouse_id') is not None:
        warehouses = [{
            "warehouse_id": data.get('warehouse_id'),
            "initial_quantity": data.get('initial_quantity', 0)
        }]

    if not name or not sku or price_raw is None:
        return jsonify({"error": "Missing required fields: name, sku, price"}), 400

    try:
        price = Decimal(str(price_raw))
        if price < 0:
            raise InvalidOperation
    except (InvalidOperation, TypeError):
        return jsonify({"error": "Invalid price"}), 400

    if not isinstance(warehouses, list) or len(warehouses) == 0:
        warehouses = []

    try:
        with db.session.begin():
            existing = db.session.execute(
                select(Product).filter_by(sku=sku)
            ).scalar_one_or_none()
            if existing:
                return jsonify({"error": "SKU already exists"}), 409

            product = Product(name=name, sku=sku, price=price)
            db.session.add(product)
            db.session.flush()

            for w in warehouses:
                wid = w.get("warehouse_id")
                qty = w.get("initial_quantity", 0)
                if wid is None:
                    continue
                wh = db.session.get(Warehouse, wid)
                if not wh:
                    return jsonify({"error": f"Warehouse {wid} does not exist"}), 400

                inv = db.session.execute(
                    select(Inventory).filter_by(product_id=product.id, warehouse_id=wid)
                ).scalar_one_or_none()
                if inv:
                    inv.quantity = inv.quantity + int(qty)
                    db.session.add(inv)
                else:
                    inv = Inventory(product_id=product.id, warehouse_id=wid, quantity=int(qty))
                    db.session.add(inv)

        return jsonify({"message": "Product created", "product_id": product.id}), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e.orig)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500