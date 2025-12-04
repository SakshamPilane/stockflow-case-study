# 🗄️ Database Design Notes
## StockFlow – Inventory Management System
## Case Study (Bynry Inc.)

This document explains the reasoning behind the database schema in schema.sql, including design choices, assumptions, and clarifying questions.

---

## 📌 1. Goals of the Schema

### The database is designed to support:
- Multiple companies using the platform
- Each company having multiple warehouses
- Products stored in multiple warehouses
- Tracking stock levels & history
- Suppliers providing products
- Bundles composed of other products
- Sales activity for forecasting and low-stock alerts

The schema must be normalized, scalable, and enforce business rules via constraints.

---

## 📁 2. Key Tables & Why They Exist
### 2.1 companies
Defines tenants of the platform.
Every warehouse, product, supplier, and sale belongs to a company.

### 2.2 warehouses
Each warehouse belongs to a company.
Indexes added for fast lookup.

### 2.3 products
Stores core product information.
Important decisions:
- UNIQUE(company_id, sku) ensures SKU uniqueness per company.
- low_stock_threshold allows overriding default thresholds.
- product_type_id links to categorical defaults.

### 2.4 inventories
This is a junction table between products and warehouses.
Reasons:
- A product can exist in multiple warehouses
- Each warehouse can store many products
- Quantity differs per warehouse
- UNIQUE(product_id, warehouse_id) prevents duplicates.

### 2.5 inventory_history
Tracks all inventory changes:
- Purchases
- Sales
- Transfers
- Adjustments

This enables:
- stock audit
- forecasting
- debugging inconsistencies
- History is append-only.

### 2.6 suppliers & supplier_products
A supplier can supply multiple products.
A product can have multiple suppliers.
We store:
- supplier SKU
- lead time
- supplier pricing
- Used in low-stock alert recommendations.

### 2.7 sales
Tracks product demand.
Used for:
- recent sales activity
- calculating average daily sales
- predicting days until stockout
- Indexed by (product_id, sold_at) for time-based queries.

### 2.8 product_bundles
Supports bundle compositions like:
A “Gift Pack” contains 2 bottle units + 1 accessory
This allows:
- nested products
- dynamic inventory deduction
- smarter forecasting

---

## ⚙️ 3. Normalization & Constraint Decisions

### ✔ Normalization Level: 3NF
- No repeated data
- Clear foreign keys
- Junction tables for many-to-many relationships

### ✔ Referencing with ON DELETE CASCADE
Used where appropriate so removing a product or warehouse cleans dependent data.

### ✔ Numeric types used for:
- price → NUMERIC(12,2)
- quantity → BIGINT

### ✔ Index strategy:
- Warehouses by company
- Products by company
- Inventory by product + warehouse
- Sales by product + sold_at
This ensures fast queries for alerts and reports.

---

## ❓ 4. Missing Requirements / Questions for Product Team
These must be clarified before building the real system.
### Are SKUs unique platform-wide or per company?
Current schema uses per-company uniqueness.

### What is the definition of “recent sales activity”?
- Last 30 days?
- Last 90 days?
- Per warehouse or company-wide?

### How should bundle products subtract inventory?
- On sale, should component quantities decrease automatically?
- How to handle partial availability of components?

### Do we support inventory transfers between warehouses?
If yes:
- Should transfers generate two history entries (+ and -)?
- Are transfers treated differently from adjustments?
Should threshold be:
- per product?
- per warehouse?
- per product type?
- or overridable at multiple levels?

### Should negative inventory be allowed?
- If yes, what business rules apply?
- If no, should operations be blocked?

### Do suppliers belong to the company or platform-wide?
- What fields must be versioned or audited?
- Product price changes?
- Supplier lead time updates?

---

## 💡 5. Design Trade-offs
### ⭐ Chosen Solution:
A normalized relational schema with clear constraints.

### Alternatives (not chosen):
- Denormalized warehouse-product documents (NoSQL)
- Stored bundles as nested JSON (less flexible)

### Relational choice is better because:
- The domain has strong relationships
- Reporting & forecasting rely on joins
- Transaction safety is critical

---

## 📈 6. Future Extensions (not required now)
The schema easily supports future features:
- Purchase orders
- Reorder automation
- Multi-currency pricing
- Forecasting using ML
- Batched inventory adjustments
- Role-based access to warehouses
