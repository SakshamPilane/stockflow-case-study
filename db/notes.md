# 🗄️ Database Design Notes  
## StockFlow – Case Study (Bynry Inc.)

These are my personal notes explaining why I designed the database the way I did.  
The goal was to support the main features of an inventory system without over-complicating things.

---

## 1) What the schema needs to support

From the case study, the system should allow:

- Multiple companies using the platform  
- Each company having multiple warehouses  
- Products stored in different warehouses with different quantities  
- Tracking inventory changes (for audit + forecasting)  
- Suppliers → which products they provide  
- Bundles (one product made of other products)  
- Sales history → used for low-stock alerts  

Basically, the schema should be clean, normalized, and work well with the APIs in Part 1 and Part 3.

---

## 2) Main tables and why they exist

### **companies**
Every record in the system belongs to a company, so this is the top-level tenant.

### **warehouses**
A company can have multiple warehouses.  
Indexed by company for fast filtering.

### **products**
Stores product info.  
Important decisions made:

- SKUs are unique **per company** (not globally).  
- `product_type_id` helps with default thresholds.  
- `low_stock_threshold` lets us override the default.

### **inventories**
This is basically the link between warehouses and products.  
A product can be stored in many warehouses, and each warehouse stores many products.

I used:
- `UNIQUE(product_id, warehouse_id)` → avoids duplicates  
- `quantity` stored as BIGINT  

### **inventory_history**
For tracking every stock change.  
This is useful later for:

- Audits  
- Debugging quantity issues  
- Forecasting trends  

This is append-only.

### **suppliers** and **supplier_products**
A supplier can supply multiple products and each product may have multiple suppliers.  
Stored info includes:

- supplier SKU  
- lead time  
- cost  

Used mainly by the low-stock alerts logic.

### **sales**
Tracks how much a product is getting sold.  
Important for:

- “recent sales activity” rule  
- average daily sales  
- stock-out prediction  

I indexed `(product_id, sold_at)` for fast lookups.

### **product_bundles**
For handling bundles like "Gift Pack contains X + Y".  
Not fully implemented in the API, but schema supports it.

---

## 3) Normalization and constraints

- Designed roughly in **3NF**  
- No duplicated fields  
- Clear foreign keys everywhere  

I used `ON DELETE CASCADE` in places where removing parent records should remove dependent entries (inventories, history, supplier-product links).

Indexes were added where the API will query the most:

- warehouses by company  
- products by company  
- inventories by product/warehouse  
- sales by product and date  

---

## 4) Requirements that were unclear (questions I would ask the product team)

The case study doesn’t specify a few important details.  
Before building the real system, I’d ask:

- Should SKUs be unique globally or per company?  
- How many days count as “recent sales”? (I assumed 90)  
- Should bundles automatically reduce component quantities when sold?  
- Can inventory go negative? Or should we block such cases?  
- Should thresholds be set per-product, per-warehouse, or type-level only?  
- Do suppliers belong only to a company, or can they be shared platform-wide?  
- Should inventory transfers between warehouses be tracked separately?  

These decisions affect both schema and API behavior.

---

## 5) Design trade-offs

I chose a **relational design** because:

- Data is highly connected  
- Queries for alerts and forecasting require joins  
- Auditing and consistency matter a lot  

Alternative could be a denormalized NoSQL design, but that would complicate relationships like bundles and suppliers.

---

## 6) Future extensions the schema can support

Not required for the case study, but the structure makes it easy to add:

- Purchase orders  
- Automated reorder suggestions  
- Warehouse-specific thresholds  
- Multi-currency pricing  
- Role-based access  
- ML-based forecasting  

These weren’t implemented, but the schema can grow into them.

---

These notes reflect my thought process while designing the schema and preparing for Part 2 of the case study.