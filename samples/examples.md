# 📄 StockFlow Case Study – Sample API Examples
This file contains mock example inputs and outputs for the API implementations in Part 1 and Part 3.
These examples illustrate how the endpoints would behave in a real system and help reviewers understand your logic.

## 🧩 Part 1 — Product Creation API

### POST /api/products
Sample Request #1 (Single Warehouse)
```json
{
  "name": "Premium Water Bottle",
  "sku": "WB-001",
  "price": 199.50,
  "warehouse_id": 10,
  "initial_quantity": 50
}
```

#### 🎯 Expected Behavior
- Checks SKU uniqueness
- Creates product
- Adds inventory for warehouse 10 → quantity: 50
- Returns success

#### Sample Response
```json
{
  "message": "Product created",
  "product_id": 101
}
```

#### Sample Request #2 (Multiple Warehouses)
```json
{
  "name": "Smart Faucet Sensor",
  "sku": "SFS-220",
  "price": 899.99,
  "warehouses": [
    { "warehouse_id": 10, "initial_quantity": 20 },
    { "warehouse_id": 12, "initial_quantity": 35 }
  ]
}
```
#### Sample Response
```json
{
  "message": "Product created",
  "product_id": 102
}
```

#### ❌ Sample Error — Missing Fields
```json
{
  "sku": "BAD-001"
}
```
#### Response (Status: 400)
```json
{
  "error": "Missing required fields: name, sku, price"
}
```

#### ❌ Sample Error — Duplicate SKU
```json
{
  "name": "Bottle",
  "sku": "WB-001",
  "price": 100
}
```
#### Response (Status: 409)
```json
{
  "error": "SKU already exists"
}
```

---

## 🔔 Part 3 — Low-Stock Alerts API

### GET /api/companies/5/alerts/low-stock

#### Example scenario:
- Product A threshold = 20
- Warehouse 1 stock = 5
- Warehouse 2 stock = 30
- Recent sales: yes
- Supplier exists with lead time = 5 days

#### 🔍 Expected Behavior:
- Alert for warehouse 1 (5 < 20)
- No alert for warehouse 2

#### ✅ Sample Response
```json
{
  "alerts": [
    {
      "product_id": 123,
      "product_name": "Premium Water Bottle",
      "sku": "WB-001",
      "warehouse_id": 10,
      "warehouse_name": "Main Warehouse",
      "current_stock": 5,
      "threshold": 20,
      "days_until_stockout": 12,
      "supplier": {
        "id": 45,
        "name": "AquaSupplies Co.",
        "contact_email": "orders@aquasupplies.com"
      }
    }
  ],
  "total_alerts": 1
}
```

#### ❌ Sample Response — No Recent Sales
If a product has low stock but NO sales in last 90 days:
```json
{
  "alerts": [],
  "total_alerts": 0
}
```

#### ❌ Sample Response — No Supplier Linked
```json
{
  "alerts": [
    {
      "product_id": 200,
      "product_name": "Sensor Module",
      "sku": "SM-909",
      "warehouse_id": 10,
      "warehouse_name": "Main Warehouse",
      "current_stock": 3,
      "threshold": 15,
      "days_until_stockout": 1,
      "supplier": null
    }
  ],
  "total_alerts": 1
}
```

#### 🧮 Days-Until-Stockout Calculation Example
If:
- current_stock = 30
- total sales in last 90 days = 180
- avg_daily_sales = 180 / 90 = 2
Then:
```ini
days_until_stockout = 30 / 2 = 15
```

