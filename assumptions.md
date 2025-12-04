# StockFlow Case Study – Backend Engineering
## Assumptions for Part 1, Part 2, and Part 3
This document lists all assumptions made during the implementation of the case study.
Since many business rules were intentionally left incomplete, these assumptions ensure consistent logic and demonstrate reasoning.

---

## 🧩 Part 1 — Product Creation API (Debugging & Fixes)

### 1. Product does not belong to a single warehouse
The original code incorrectly stored warehouse_id inside Product.
I assume:
- A product can exist in multiple warehouses, so inventory is stored separately in the inventories table.

### 2. SKU uniqueness
The instructions say “SKUs must be unique across the platform” but realistic SaaS platforms usually allow different companies to use the same SKU.
I assume:
- SKUs must be unique per company, not globally.
(If truly global uniqueness is required, the schema can be updated.)

### 3. Price handling
Price may be decimal, so float types should not be used.
I assume:
- Price is validated as Decimal and stored as NUMERIC(12,2).

### 4. Optional warehouses in request
The request may include:
- a single warehouse (warehouse_id, initial_quantity)
- OR a list of warehouses (warehouses: [])
- OR none at all

I assume:
- If no warehouse is provided, product is created with zero inventory.

### 5. Inventory upsert behavior
If inventory already exists for (product, warehouse):
- Quantity is increased by initial_quantity instead of creating a duplicate row.

### 6. Atomic transaction requirement
The original code had two commits, which could leave half-created data.
I assume:
- Product creation + inventory creation must succeed or fail as a single transaction.

### 7. Error responses
I assume:
- Missing required fields → 400 Bad Request
- Duplicate SKU → 409 Conflict
- DB constraint errors → 500 Internal Server Error

---

## 🗄️ Part 2 — Database Design Assumptions

### 1. SKU uniqueness scope
As above:
- SKU uniqueness is enforced per company.

### 2. Inventory belongs to product + warehouse
Inventory is a many-to-many relationship.
- One product can exist in multiple warehouses
- A warehouse can store many products

### 3. Inventory history is append-only
I assume:
- No updates — only inserts
- Used for audits and forecasting (sales velocity)

### 4. Bundles require component deduction
The prompt states bundles exist but does not define how inventory should change.
I assume:
- Bundles will eventually subtract component product quantities.
- This is not implemented here because rules are incomplete.

### 5. Supplier logic
I assume:
- Suppliers belong to companies
- A product may have multiple suppliers
- Supplier with shortest lead time is preferred for re-order alerts

### 6. Sales activity
The prompt says "recent sales activity" but gives no timeframe.
I assume:
- Recent sales = sales within last 90 days
- Sales lookback period for forecasting = 90 days

### 7. Low-stock thresholds
The prompt says thresholds vary by product type.
I assume:
- If low_stock_threshold is set on product → use it
- Else use product type default
- Else fallback threshold = 10

---

## 🔔 Part 3 — Low-Stock Alerts API Assumptions

### 1. days_until_stockout formula
Prompt doesn’t define how to compute this.
I assume:
- days_until_stockout = current_stock / avg_daily_sales
- If avg_daily_sales = 0 → output null

### 2. Filtering by recent sales
Prompt says only alert if product has recent sales.
I assume:
- Must have at least 1 sale in last 90 days (company-wide).
- Not restricted to warehouse-specific sales.

### 3. Supplier selection
When multiple suppliers exist, prompt does not define selection rule.
I assume:
- Choose supplier with shortest lead time.

### 4. Multi-warehouse logic
Prompt says alerts must support multiple warehouses.
I assume:
- Each warehouse generates its own alert entry.
- Only include warehouses where quantity < threshold.

### 5. Missing supplier
I assume:
- If no supplier exists for product → supplier: null.

### 6. Units and currencies
The problem does not specify any units.
I assume:
- Quantity is integer (units)
- Price is stored in company’s base currency
