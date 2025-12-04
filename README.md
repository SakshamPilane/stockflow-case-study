# 📦 StockFlow Case Study – Backend Engineering (Bynry Inc.)
## Candidate: Saksham Pilane
This repository contains my solution for the StockFlow (B2B Inventory Management) case study.
It includes a corrected product creation endpoint, a database schema, and an implementation plan + code for the low-stock alerts API.
The submission focuses on correct backend logic, DB design, and clear assumptions rather than a full runnable app.

---

### 📂 What’s in this repo
```pqsql
stockflow-case-study/
│
├── README.md
├── case_study_solution.md      <-- Full write-up for the Google form
├── assumptions.md              <-- All assumptions made for Parts 1–3
│
├── part1_fixed_create_product.py
├── part3_low_stock_alerts.py
│
├── app.py                      <-- lightweight placeholders to satisfy imports
├── models.py                   <-- minimal SQLAlchemy models for structure
│
├── db/
│   ├── schema.sql              <-- SQL DDL (tables, constraints, indexes)
│   └── notes.md                <-- design notes, decisions, missing requirements
│
└── samples/
    └── examples.md             <-- sample requests & responses (mocked)
```

---

## ✅ How This Repo Satisfies the Case Study Requirements

### ✔ Part 1 — Code Review & Debugging
- Identified ALL issues in original endpoint (technical + business logic)
- Implemented corrected API with:
  - SKU uniqueness validation  
  - Decimal-based price handling  
  - Proper warehouse handling  
  - Transaction-safe product + inventory creation  
  - Upsert logic for existing inventory  
  - Clean status codes and error handling  
- Code in: **`part1_fixed_create_product.py`**

### ✔ Part 2 — Database Schema Design
- Designed normalized SQL schema covering:
  - Multi-company tenancy
  - Multiple warehouses per company
  - Product inventory across warehouses
  - Inventory history/audit logging
  - Supplier relationships + lead time
  - Product bundles
  - Sales history for forecasting alerts  
- Indexes + constraints included  
- Schema & decisions in:
  - **`db/schema.sql`**
  - **`db/notes.md`**

### ✔ Part 3 — Low-Stock Alerts API
- Implements `GET /api/companies/{id}/alerts/low-stock`
- Handles:
  - Product-level or type-level thresholds
  - Multi-warehouse filtering
  - Recent sales activity (last 90 days)
  - Supplier selection with shortest lead-time
  - Days-until-stockout calculation
- Code in: **`part3_low_stock_alerts.py`**
- Examples in: **`samples/examples.md`**

### ✔ Assumptions (required for incomplete requirements)
All assumptions documented in:
- **`assumptions.md`**

---

## 🧾 Quick Reviewer Checklist

This submission includes:

- [x] Explanation of bugs in original API
- [x] Corrected version with validation + transactions
- [x] Normalized SQL schema with relationships
- [x] Indexes and constraints for scaling
- [x] Low-stock alert logic with reasoning
- [x] Edge-case handling
- [x] Thoughts on missing requirements
- [x] Documented assumptions
- [x] Sample request/response examples
- [x] Cleanly structured repo
