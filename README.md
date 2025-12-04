# 📦 StockFlow Case Study – Backend Engineering (Bynry Inc.)
## Candidate: Saksham Maruti Pilane

📄 **Full Write-Up (All Parts Explained):**  
👉 [`case_study_solution.md`](./case_study_solution.md)

This repository contains my solution for the StockFlow (B2B Inventory Management) case study.  
It includes a corrected product creation endpoint, a database schema, and an implementation plan + code for the low-stock alerts API.  
The submission focuses on correct backend logic, DB design, and clear assumptions rather than a full runnable app.

---

### 📂 What’s in this repo

| File / Folder | Description |
|--------------|-------------|
| [`case_study_solution.md`](./case_study_solution.md) | Full write-up for the Google form (all parts: reasoning + explanations) |
| [`assumptions.md`](./assumptions.md) | Documented assumptions for Parts 1–3 |
| [`part1_fixed_create_product.py`](./part1_fixed_create_product.py) | Corrected product creation API |
| [`part3_low_stock_alerts.py`](./part3_low_stock_alerts.py) | Low-stock alerts API implementation |
| [`app.py`](./app.py) | Lightweight placeholder for imports |
| [`models.py`](./models.py) | Minimal models for schema reference |
| [`db/schema.sql`](./db/schema.sql) | Full SQL schema with indexes & constraints |
| [`db/notes.md`](./db/notes.md) | Schema decisions, gaps, and rationale |
| [`db/erd.puml`](./db/erd.puml) | ERD (PlantUML source) |
| `db/erd.png` | *(Add after generating PNG from puml file)* |
| [`samples/examples.md`](./samples/examples.md) | Mocked API requests & responses |

---

## 🧭 Entity Relationship Diagram (ERD)

A complete ERD for the StockFlow inventory system is available here:

📌 **PlantUML Source:**  
👉 [`db/erd.puml`](./db/erd.puml)

📌 **Rendered Diagram (PNG):**  
👉 *(Add `erd.png` here once generated)*

To generate the ERD:

1. Open https://www.plantuml.com/plantuml/uml  
2. Paste the contents of `db/erd.puml`  
3. Export as `.png`  
4. Place the image at: `db/erd.png`

---

## 🎤 What to Expect in the Live Technical Discussion

During the live session, I am prepared to walk through:

### **1. Part 1 – Debugging Thought-Process**
- Bugs identified in the original endpoint  
- Impact in production  
- How the corrected version fixes each issue  
- Why certain backend/API design choices were made  

### **2. Part 2 – Database Design Trade-offs**
- Normalization approach  
- Why certain relationships & constraints were chosen  
- How schema supports scaling + multi-tenancy  
- Missing requirements & questions I would ask the product team  

### **3. Part 3 – Low-Stock Alerts API**
- How thresholds are determined  
- Why recent-sales logic matters  
- Forecasting stock-out (days until depletion)  
- Supplier selection strategy  
- Edge-case handling  

---

## ✅ How This Repo Satisfies the Case Study Requirements

### ✔ Part 1 — Code Review & Debugging  
Corrected implementation:  
👉 [`part1_fixed_create_product.py`](./part1_fixed_create_product.py)

Fixes include:
- SKU uniqueness validation  
- Decimal-safe pricing  
- Multi-warehouse support  
- Transaction-safe product & inventory creation  
- Upsert logic  
- Error handling & HTTP status codes  

---

### ✔ Part 2 — Database Schema Design  
SQL schema:  
👉 [`db/schema.sql`](./db/schema.sql)  
Design notes:  
👉 [`db/notes.md`](./db/notes.md)

Covers:
- Multi-company tenancy  
- Warehouses per company  
- Inventory tracking  
- Supplier relationships  
- Bundles  
- Inventory history & sales  

---

### ✔ Part 3 — Low-Stock Alerts API  
Implementation:  
👉 [`part3_low_stock_alerts.py`](./part3_low_stock_alerts.py)

Handles:
- Type-based and product-level thresholds  
- Multi-warehouse filtering  
- Recent sales validation  
- Supplier lookup (shortest lead time)  
- Days-until-stockout calculation  

Mock request/response examples:  
👉 [`samples/examples.md`](./samples/examples.md)

---

### ✔ Assumptions (for incomplete requirements)  
👉 [`assumptions.md`](./assumptions.md)

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
- [x] Clean, organized repository structure  
