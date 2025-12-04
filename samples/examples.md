# 📄 Sample API Examples (My Notes)

These are a few mock examples I created to show how my Part 1 and Part 3 APIs would behave.  
They’re not real outputs — just to help explain the logic.

---

## Part 1 — Product Creation API

### POST /api/products

### Example 1: Single Warehouse
```json
{
  "name": "Premium Water Bottle",
  "sku": "WB-001",
  "price": 199.50,
  "warehouse_id": 10,
  "initial_quantity": 50
}
```

Expected:
- Valid request  
- Product created  
- Inventory row added for warehouse 10  

Response:
```json
{
  "message": "Product created",
  "product_id": 101
}
```

---

### Example 2: Multiple Warehouses
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

Response:
```json
{
  "message": "Product created",
  "product_id": 102
}
```

---

### Missing Required Fields
```json
{
  "sku": "BAD-001"
}
```

Response (400):
```json
{
  "error": "Missing required fields: name, sku, price"
}
```

---

### Duplicate SKU
```json
{
  "name": "Bottle",
  "sku": "WB-001",
  "price": 100
}
```

Response (409):
```json
{
  "error": "SKU already exists"
}
```

---

### Invalid Warehouse ID (extra example)
```json
{
  "name": "Test",
  "sku": "T-1",
  "price": 50,
  "warehouse_id": 999,
  "initial_quantity": 10
}
```

Response:
```json
{
  "error": "Warehouse 999 does not exist"
}
```

---

## Part 3 — Low-Stock Alerts API

### GET /api/companies/5/alerts/low-stock

Example scenario:
- Product threshold = 20  
- Warehouse 1 → stock = 5  
- Warehouse 2 → stock = 30  
- Only warehouse 1 should trigger an alert  

Sample Response:
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

---

### No Recent Sales
```json
{
  "alerts": [],
  "total_alerts": 0
}
```

---

### No Supplier Found
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

---

### Days-Until-Stockout Calculation Example
If:
- Stock = 30  
- Sold 180 in last 90 days  
- Avg daily sales = 180 / 90 = 2  

Then:
```
days_until_stockout = 30 / 2 = 15
```