# part3_low_stock_alerts.py
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from sqlalchemy import func
from app import db
from models import (
    Company, Product, Inventory, Warehouse,
    Sale, Supplier, SupplierProduct
)

app = Flask(__name__)

RECENT_SALES_DAYS = 90
SALES_LOOKBACK_DAYS = 90
DEFAULT_THRESHOLD_BY_TYPE = {
    1: 10,
    2: 20,
    3: 50
}
FALLBACK_THRESHOLD = 10


@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    """
    Part 3 — Low Stock Alerts Endpoint
    Includes:
    - multi-warehouse filtering
    - recent sales validation
    - threshold calculation from product type OR product override
    - supplier lookup by shortest lead time
    - stockout forecast calculation
    """

    company = db.session.get(Company, company_id)
    if not company:
        return jsonify({"error": f"Company {company_id} does not exist"}), 404

    recent_days = int(request.args.get("recent_days", RECENT_SALES_DAYS))
    sales_lookback = int(request.args.get("sales_lookback", SALES_LOOKBACK_DAYS))

    cutoff_recent = datetime.utcnow() - timedelta(days=recent_days)
    sales_from = datetime.utcnow() - timedelta(days=sales_lookback)

    q = (
        db.session.query(Inventory, Product, Warehouse)
        .join(Product, Inventory.product_id == Product.id)
        .join(Warehouse, Inventory.warehouse_id == Warehouse.id)
        .filter(
            Product.company_id == company_id,
            Warehouse.company_id == company_id
        )
    )

    alerts = []

    for inv, prod, wh in q:

        if prod.low_stock_threshold is not None:
            threshold = prod.low_stock_threshold
        elif prod.product_type_id is not None:
            threshold = DEFAULT_THRESHOLD_BY_TYPE.get(
                prod.product_type_id,
                FALLBACK_THRESHOLD
            )
        else:
            threshold = FALLBACK_THRESHOLD

        current_stock = inv.quantity

        if current_stock < 0:
            days_until_stockout = 0
            alerts.append({
                "product_id": prod.id,
                "product_name": prod.name,
                "sku": prod.sku,
                "warehouse_id": wh.id,
                "warehouse_name": wh.name,
                "current_stock": int(current_stock),
                "threshold": int(threshold),
                "days_until_stockout": days_until_stockout,
                "supplier": None
            })
            continue

        if current_stock >= threshold:
            continue

        recent_sales_count = (
            db.session.query(func.count(Sale.id))
            .filter(
                Sale.product_id == prod.id,
                Sale.company_id == company_id,
                Sale.sold_at >= cutoff_recent
            )
            .scalar()
        )

        if recent_sales_count == 0:
            continue

        total_sold = (
            db.session.query(func.coalesce(func.sum(Sale.quantity), 0))
            .filter(
                Sale.product_id == prod.id,
                Sale.company_id == company_id,
                Sale.sold_at >= sales_from
            )
            .scalar()
        ) or 0

        days_window = max(1, sales_lookback)
        avg_daily_sales = total_sold / days_window

        if avg_daily_sales > 0:
            days_until_stockout = int(current_stock / avg_daily_sales)
        else:
            days_until_stockout = None

        sup_row = (
            db.session.query(Supplier, SupplierProduct)
            .join(SupplierProduct, Supplier.id == SupplierProduct.supplier_id)
            .filter(
                SupplierProduct.product_id == prod.id,
                Supplier.company_id == company_id
            )
            .order_by(SupplierProduct.lead_time_days.asc())
            .first()
        )

        supplier_obj = None
        if sup_row:
            supplier, sup_prod = sup_row
            supplier_obj = {
                "id": supplier.id,
                "name": supplier.name,
                "contact_email": supplier.contact_email
            }

        alerts.append({
            "product_id": prod.id,
            "product_name": prod.name,
            "sku": prod.sku,
            "warehouse_id": wh.id,
            "warehouse_name": wh.name,
            "current_stock": int(current_stock),
            "threshold": int(threshold),
            "days_until_stockout": days_until_stockout,
            "supplier": supplier_obj
        })

    return jsonify({"alerts": alerts, "total_alerts": len(alerts)}), 200
