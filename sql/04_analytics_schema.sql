-- ============================================================
-- FLOWCHAIN
-- REAL SUPPLY CHAIN ANALYTICS SCHEMA
-- Based on 91,250-row Kaggle dataset
-- ============================================================


-- ============================================================
-- 1. ANALYTICAL SUPPLIERS
-- ============================================================

CREATE TABLE IF NOT EXISTS SC_Suppliers (
    SupplierID VARCHAR(20) PRIMARY KEY,
    SupplierLeadTimeDays INTEGER NOT NULL
);


-- ============================================================
-- 2. ANALYTICAL WAREHOUSES
-- ============================================================

CREATE TABLE IF NOT EXISTS SC_Warehouses (
    WarehouseID VARCHAR(20) PRIMARY KEY,
    Region VARCHAR(50) NOT NULL
);


-- ============================================================
-- 3. ANALYTICAL PRODUCTS
-- ============================================================

CREATE TABLE IF NOT EXISTS SC_Products (
    SKU_ID VARCHAR(20) PRIMARY KEY,
    SupplierID VARCHAR(20) NOT NULL,
    UnitCost DECIMAL(10,2) NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_sc_product_supplier
        FOREIGN KEY (SupplierID)
        REFERENCES SC_Suppliers(SupplierID)
);


-- ============================================================
-- 4. SALES
-- ============================================================

CREATE TABLE IF NOT EXISTS SC_Sales (
    SaleID BIGSERIAL PRIMARY KEY,

    SaleDate DATE NOT NULL,
    SKU_ID VARCHAR(20) NOT NULL,
    WarehouseID VARCHAR(20) NOT NULL,

    UnitsSold INTEGER NOT NULL,

    UnitCost DECIMAL(10,2) NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,

    PromotionFlag INTEGER NOT NULL DEFAULT 0,

    Revenue DECIMAL(14,2) NOT NULL,
    Cost DECIMAL(14,2) NOT NULL,
    Profit DECIMAL(14,2) NOT NULL,
    ProfitMargin DECIMAL(8,2),

    CONSTRAINT fk_sc_sales_product
        FOREIGN KEY (SKU_ID)
        REFERENCES SC_Products(SKU_ID),

    CONSTRAINT fk_sc_sales_warehouse
        FOREIGN KEY (WarehouseID)
        REFERENCES SC_Warehouses(WarehouseID)
);


-- ============================================================
-- 5. INVENTORY
-- ============================================================

CREATE TABLE IF NOT EXISTS SC_Inventory (
    InventoryID BIGSERIAL PRIMARY KEY,

    InventoryDate DATE NOT NULL,
    SKU_ID VARCHAR(20) NOT NULL,
    WarehouseID VARCHAR(20) NOT NULL,

    InventoryLevel INTEGER NOT NULL,
    ReorderPoint INTEGER NOT NULL,
    LowStockFlag INTEGER NOT NULL,

    CONSTRAINT fk_sc_inventory_product
        FOREIGN KEY (SKU_ID)
        REFERENCES SC_Products(SKU_ID),

    CONSTRAINT fk_sc_inventory_warehouse
        FOREIGN KEY (WarehouseID)
        REFERENCES SC_Warehouses(WarehouseID)
);


-- ============================================================
-- 6. DEMAND FORECAST
-- ============================================================

CREATE TABLE IF NOT EXISTS SC_DemandForecast (
    ForecastID BIGSERIAL PRIMARY KEY,

    ForecastDate DATE NOT NULL,
    SKU_ID VARCHAR(20) NOT NULL,
    WarehouseID VARCHAR(20) NOT NULL,

    ActualDemand INTEGER NOT NULL,
    ForecastedDemand DECIMAL(10,2) NOT NULL,

    ForecastError DECIMAL(10,2),
    AbsoluteForecastError DECIMAL(10,2),

    CONSTRAINT fk_sc_forecast_product
        FOREIGN KEY (SKU_ID)
        REFERENCES SC_Products(SKU_ID),

    CONSTRAINT fk_sc_forecast_warehouse
        FOREIGN KEY (WarehouseID)
        REFERENCES SC_Warehouses(WarehouseID)
);


-- ============================================================
-- 7. REPLENISHMENT ORDERS
-- ============================================================

CREATE TABLE IF NOT EXISTS SC_ReplenishmentOrders (
    ReplenishmentID BIGSERIAL PRIMARY KEY,

    OrderDate DATE NOT NULL,
    SKU_ID VARCHAR(20) NOT NULL,
    WarehouseID VARCHAR(20) NOT NULL,
    SupplierID VARCHAR(20) NOT NULL,

    OrderQuantity INTEGER NOT NULL,

    CONSTRAINT fk_sc_replenishment_product
        FOREIGN KEY (SKU_ID)
        REFERENCES SC_Products(SKU_ID),

    CONSTRAINT fk_sc_replenishment_warehouse
        FOREIGN KEY (WarehouseID)
        REFERENCES SC_Warehouses(WarehouseID),

    CONSTRAINT fk_sc_replenishment_supplier
        FOREIGN KEY (SupplierID)
        REFERENCES SC_Suppliers(SupplierID)
);


-- ============================================================
-- 8. INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_sc_sales_date
ON SC_Sales(SaleDate);

CREATE INDEX IF NOT EXISTS idx_sc_sales_sku
ON SC_Sales(SKU_ID);

CREATE INDEX IF NOT EXISTS idx_sc_sales_warehouse
ON SC_Sales(WarehouseID);


CREATE INDEX IF NOT EXISTS idx_sc_inventory_date
ON SC_Inventory(InventoryDate);

CREATE INDEX IF NOT EXISTS idx_sc_inventory_sku
ON SC_Inventory(SKU_ID);


CREATE INDEX IF NOT EXISTS idx_sc_forecast_date
ON SC_DemandForecast(ForecastDate);

CREATE INDEX IF NOT EXISTS idx_sc_forecast_sku
ON SC_DemandForecast(SKU_ID);


CREATE INDEX IF NOT EXISTS idx_sc_replenishment_date
ON SC_ReplenishmentOrders(OrderDate);

CREATE INDEX IF NOT EXISTS idx_sc_replenishment_sku
ON SC_ReplenishmentOrders(SKU_ID);


-- ============================================================
-- SCHEMA COMPLETE
-- ============================================================