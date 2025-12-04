# part1_fixed_create_product.py
from decimal import Decimal, InvalidOperation
from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app import db
from models import Product, Inventory, Warehouse

app = Flask(__name__)

@app.route('/api/products', methods=['POST'])
def create_product():
    """
    Part 1 — Corrected Product Creation Endpoint
    Includes:
    - company_id support
    - SKU uniqueness per company
    - warehouse validation
    - inventory upsert logic
    - atomic transaction
    """

    data = request.get_json() or {}

    name = data.get("name")
    sku = data.get("sku")
    price_raw = data.get("price")
    company_id = data.get("company_id")

    if not company_id:
        return jsonify({"error": "Missing required field: company_id"}), 400

    if not name or not sku or price_raw is None:
        return jsonify({"error": "Missing required fields: name, sku, price"}), 400

    try:
        price = Decimal(str(price_raw))
        if price < 0:
            raise InvalidOperation
    except (InvalidOperation, TypeError):
        return jsonify({"error": "Invalid price"}), 400

    warehouses = data.get("warehouses")

    if not warehouses and data.get("warehouse_id") is not None:
        warehouses = [{
            "warehouse_id": data.get("warehouse_id"),
            "initial_quantity": data.get("initial_quantity", 0)
        }]

    if not isinstance(warehouses, list) or len(warehouses) == 0:
        warehouses = []

    try:
        with db.session.begin():

            existing = db.session.execute(
                select(Product).filter_by(company_id=company_id, sku=sku)
            ).scalar_one_or_none()

            if existing:
                return jsonify({"error": "SKU already exists for this company"}), 409

            product = Product(
                name=name,
                sku=sku,
                price=price,
                company_id=company_id
            )
            db.session.add(product)
            db.session.flush()

            for w in warehouses:
                wid = w.get("warehouse_id")
                qty = int(w.get("initial_quantity", 0))

                if wid is None:
                    continue

                wh = db.session.get(Warehouse, wid)
                if not wh:
                    return jsonify({"error": f"Warehouse {wid} does not exist"}), 400
                
                if wh.company_id != company_id:
                    return jsonify({"error": f"Warehouse {wid} does not belong to company {company_id}"}), 400

                inv = db.session.execute(
                    select(Inventory).filter_by(product_id=product.id, warehouse_id=wid)
                ).scalar_one_or_none()

                if inv:
                    inv.quantity = inv.quantity + qty
                    db.session.add(inv)
                else:
                    inv = Inventory(
                        product_id=product.id,
                        warehouse_id=wid,
                        quantity=qty
                    )
                    db.session.add(inv)

        return jsonify({
            "message": "Product created",
            "product_id": product.id
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            "error": "Database integrity error",
            "details": str(e.orig)
        }), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500