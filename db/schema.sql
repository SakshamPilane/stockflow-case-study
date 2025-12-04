-- Companies
CREATE TABLE companies (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Warehouses -> Company
CREATE TABLE warehouses (
  id BIGSERIAL PRIMARY KEY,
  company_id BIGINT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  address TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE INDEX idx_warehouses_company ON warehouses(company_id);

-- Product types
CREATE TABLE product_types (
  id SMALLINT PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

-- Products
CREATE TABLE products (
  id BIGSERIAL PRIMARY KEY,
  company_id BIGINT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  sku VARCHAR(128) NOT NULL,
  description TEXT,
  price NUMERIC(12,2) NOT NULL,
  product_type_id SMALLINT REFERENCES product_types(id),
  low_stock_threshold INT DEFAULT NULL,
  is_bundle BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  UNIQUE (company_id, sku)
);

CREATE INDEX idx_products_company ON products(company_id);

-- Inventory: mapping product <-> warehouse, with current quantity
CREATE TABLE inventories (
  id BIGSERIAL PRIMARY KEY,
  product_id BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  warehouse_id BIGINT NOT NULL REFERENCES warehouses(id) ON DELETE CASCADE,
  quantity BIGINT NOT NULL DEFAULT 0,
  last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  UNIQUE (product_id, warehouse_id)
);
CREATE INDEX idx_inventories_product ON inventories(product_id);
CREATE INDEX idx_inventories_warehouse ON inventories(warehouse_id);

-- Inventory history / audit logs
CREATE TABLE inventory_history (
  id BIGSERIAL PRIMARY KEY,
  inventory_id BIGINT NOT NULL REFERENCES inventories(id) ON DELETE CASCADE,
  change BIGINT NOT NULL,
  reason VARCHAR(255),
  reference_id BIGINT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  created_by BIGINT
);
CREATE INDEX idx_invhist_inventory ON inventory_history(inventory_id);

-- Suppliers
CREATE TABLE suppliers (
  id BIGSERIAL PRIMARY KEY,
  company_id BIGINT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  contact_email VARCHAR(255),
  phone VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Supplier-Product relations (many-to-many)
CREATE TABLE supplier_products (
  id BIGSERIAL PRIMARY KEY,
  supplier_id BIGINT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  product_id BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  supplier_sku VARCHAR(128),
  lead_time_days INT DEFAULT 7,
  price NUMERIC(12,2),
  UNIQUE (supplier_id, product_id)
);

-- Sales table to track recent sales
CREATE TABLE sales (
  id BIGSERIAL PRIMARY KEY,
  company_id BIGINT NOT NULL REFERENCES companies(id),
  product_id BIGINT NOT NULL REFERENCES products(id),
  warehouse_id BIGINT REFERENCES warehouses(id),
  quantity BIGINT NOT NULL,
  total_amount NUMERIC(12,2),
  sold_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE INDEX idx_sales_product_soldat ON sales(product_id, sold_at DESC);

-- Bundles (composition): If product A is a bundle, what's inside it
CREATE TABLE product_bundles (
  bundle_id BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  component_product_id BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  quantity INT NOT NULL DEFAULT 1,
  PRIMARY KEY (bundle_id, component_product_id)
);