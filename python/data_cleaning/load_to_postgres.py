import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from pathlib import Path
import getpass


# ============================================================
# FLOWCHAIN - POSTGRESQL ETL LOADER
# ============================================================

print("=" * 70)
print("FLOWCHAIN - POSTGRESQL ETL LOADER")
print("=" * 70)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "cleaned"
    / "supply_chain_cleaned.csv"
)

print("\n📂 Dataset:")
print(CSV_FILE)


if not CSV_FILE.exists():
    print("\n❌ Cleaned dataset not found!")
    print("Expected location:")
    print(CSV_FILE)
    raise SystemExit


# ============================================================
# 2. LOAD CLEANED DATASET
# ============================================================

print("\n📊 Loading cleaned dataset...")

df = pd.read_csv(CSV_FILE)

print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")


# ============================================================
# 3. DATABASE CONNECTION DETAILS
# ============================================================

print("\n🔐 PostgreSQL connection")

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "flowchain"
DB_USER = "postgres"

DB_PASSWORD = getpass.getpass(
    "Enter PostgreSQL password: "
)


# ============================================================
# 4. CONNECT TO POSTGRESQL
# ============================================================

try:

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    conn.autocommit = False

    print("\n✅ Connected to PostgreSQL")

except Exception as e:

    print("\n❌ Database connection failed!")
    print(e)
    raise SystemExit


cursor = conn.cursor()


# ============================================================
# 5. PREPARE SUPPLIERS
# ============================================================

print("\n🚚 Preparing suppliers...")

suppliers = (
    df[
        [
            "Supplier_ID",
            "Supplier_Lead_Time_Days"
        ]
    ]
    .drop_duplicates(subset=["Supplier_ID"])
    .copy()
)

supplier_records = [
    (
        row.Supplier_ID,
        int(row.Supplier_Lead_Time_Days)
    )
    for row in suppliers.itertuples(index=False)
]


# ============================================================
# 6. PREPARE WAREHOUSES
# ============================================================

print("🏭 Preparing warehouses...")

# A warehouse may appear with multiple regions in the dataset.
# We use the most frequently occurring region for each warehouse.

warehouse_region = (
    df.groupby("Warehouse_ID")["Region"]
    .agg(lambda x: x.mode().iloc[0])
    .reset_index()
)

warehouse_records = [
    (
        row.Warehouse_ID,
        row.Region
    )
    for row in warehouse_region.itertuples(index=False)
]


# ============================================================
# 7. PREPARE PRODUCTS
# ============================================================

print("📦 Preparing products...")

# Check whether a SKU is associated with multiple suppliers.

supplier_conflicts = (
    df.groupby("SKU_ID")["Supplier_ID"]
    .nunique()
)

conflicting_skus = supplier_conflicts[
    supplier_conflicts > 1
]

if len(conflicting_skus) > 0:

    print(
        "\n⚠️ Warning:"
        f" {len(conflicting_skus)} SKUs have multiple suppliers."
    )

    print(
        "Using the most frequently occurring supplier for each SKU."
    )


product_data = (
    df.groupby("SKU_ID")
    .agg(
        SupplierID=("Supplier_ID", lambda x: x.mode().iloc[0]),
        UnitCost=("Unit_Cost", "mean"),
        UnitPrice=("Unit_Price", "mean")
    )
    .reset_index()
)

product_records = [
    (
        row.SKU_ID,
        row.SupplierID,
        round(float(row.UnitCost), 2),
        round(float(row.UnitPrice), 2)
    )
    for row in product_data.itertuples(index=False)
]


# ============================================================
# 8. PREPARE SALES
# ============================================================

print("💰 Preparing sales records...")

sales_records = [
    (
        row.Date,
        row.SKU_ID,
        row.Warehouse_ID,
        int(row.Units_Sold),
        round(float(row.Unit_Cost), 2),
        round(float(row.Unit_Price), 2),
        int(row.Promotion_Flag),
        round(float(row.Revenue), 2),
        round(float(row.Cost), 2),
        round(float(row.Profit), 2),
        round(float(row.Profit_Margin), 2)
    )
    for row in df.itertuples(index=False)
]


# ============================================================
# 9. PREPARE INVENTORY
# ============================================================

print("📦 Preparing inventory records...")

inventory_records = [
    (
        row.Date,
        row.SKU_ID,
        row.Warehouse_ID,
        int(row.Inventory_Level),
        int(row.Reorder_Point),
        int(row.Low_Stock_Flag)
    )
    for row in df.itertuples(index=False)
]


# ============================================================
# 10. PREPARE DEMAND FORECAST
# ============================================================

print("🔮 Preparing demand forecast records...")

forecast_records = [
    (
        row.Date,
        row.SKU_ID,
        row.Warehouse_ID,
        int(row.Units_Sold),
        round(float(row.Demand_Forecast), 2),
        round(float(row.Forecast_Error), 2),
        round(float(row.Absolute_Forecast_Error), 2)
    )
    for row in df.itertuples(index=False)
]


# ============================================================
# 11. PREPARE REPLENISHMENT ORDERS
# ============================================================

print("🔄 Preparing replenishment records...")

replenishment_df = df[
    df["Order_Quantity"] > 0
].copy()

replenishment_records = [
    (
        row.Date,
        row.SKU_ID,
        row.Warehouse_ID,
        row.Supplier_ID,
        int(row.Order_Quantity)
    )
    for row in replenishment_df.itertuples(index=False)
]


# ============================================================
# 12. INSERT SUPPLIERS
# ============================================================

print("\n⬆️ Loading suppliers...")

execute_values(
    cursor,
    """
    INSERT INTO SC_Suppliers
    (
        SupplierID,
        SupplierLeadTimeDays
    )
    VALUES %s
    ON CONFLICT (SupplierID)
    DO UPDATE SET
        SupplierLeadTimeDays =
        EXCLUDED.SupplierLeadTimeDays
    """,
    supplier_records
)

print(f"   ✅ {len(supplier_records)} suppliers loaded")


# ============================================================
# 13. INSERT WAREHOUSES
# ============================================================

print("⬆️ Loading warehouses...")

execute_values(
    cursor,
    """
    INSERT INTO SC_Warehouses
    (
        WarehouseID,
        Region
    )
    VALUES %s
    ON CONFLICT (WarehouseID)
    DO UPDATE SET
        Region = EXCLUDED.Region
    """,
    warehouse_records
)

print(f"   ✅ {len(warehouse_records)} warehouses loaded")


# ============================================================
# 14. INSERT PRODUCTS
# ============================================================

print("⬆️ Loading products...")

execute_values(
    cursor,
    """
    INSERT INTO SC_Products
    (
        SKU_ID,
        SupplierID,
        UnitCost,
        UnitPrice
    )
    VALUES %s
    ON CONFLICT (SKU_ID)
    DO UPDATE SET
        SupplierID = EXCLUDED.SupplierID,
        UnitCost = EXCLUDED.UnitCost,
        UnitPrice = EXCLUDED.UnitPrice
    """,
    product_records
)

print(f"   ✅ {len(product_records)} products loaded")


# ============================================================
# 15. INSERT SALES
# ============================================================

print("⬆️ Loading sales...")

execute_values(
    cursor,
    """
    INSERT INTO SC_Sales
    (
        SaleDate,
        SKU_ID,
        WarehouseID,
        UnitsSold,
        UnitCost,
        UnitPrice,
        PromotionFlag,
        Revenue,
        Cost,
        Profit,
        ProfitMargin
    )
    VALUES %s
    """,
    sales_records,
    page_size=5000
)

print(f"   ✅ {len(sales_records):,} sales records loaded")


# ============================================================
# 16. INSERT INVENTORY
# ============================================================

print("⬆️ Loading inventory...")

execute_values(
    cursor,
    """
    INSERT INTO SC_Inventory
    (
        InventoryDate,
        SKU_ID,
        WarehouseID,
        InventoryLevel,
        ReorderPoint,
        LowStockFlag
    )
    VALUES %s
    """,
    inventory_records,
    page_size=5000
)

print(
    f"   ✅ {len(inventory_records):,} inventory records loaded"
)


# ============================================================
# 17. INSERT DEMAND FORECAST
# ============================================================

print("⬆️ Loading demand forecasts...")

execute_values(
    cursor,
    """
    INSERT INTO SC_DemandForecast
    (
        ForecastDate,
        SKU_ID,
        WarehouseID,
        ActualDemand,
        ForecastedDemand,
        ForecastError,
        AbsoluteForecastError
    )
    VALUES %s
    """,
    forecast_records,
    page_size=5000
)

print(
    f"   ✅ {len(forecast_records):,} forecast records loaded"
)


# ============================================================
# 18. INSERT REPLENISHMENT ORDERS
# ============================================================

print("⬆️ Loading replenishment orders...")

execute_values(
    cursor,
    """
    INSERT INTO SC_ReplenishmentOrders
    (
        OrderDate,
        SKU_ID,
        WarehouseID,
        SupplierID,
        OrderQuantity
    )
    VALUES %s
    """,
    replenishment_records,
    page_size=5000
)

print(
    f"   ✅ {len(replenishment_records):,} "
    "replenishment records loaded"
)


# ============================================================
# 19. COMMIT TRANSACTION
# ============================================================

conn.commit()

print("\n" + "=" * 70)
print("🎉 ETL COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\n📊 PostgreSQL Summary")

print(f"Suppliers              : {len(supplier_records):,}")
print(f"Warehouses             : {len(warehouse_records):,}")
print(f"Products               : {len(product_records):,}")
print(f"Sales                  : {len(sales_records):,}")
print(f"Inventory              : {len(inventory_records):,}")
print(f"Demand Forecast        : {len(forecast_records):,}")
print(f"Replenishment Orders   : {len(replenishment_records):,}")


# ============================================================
# 20. CLOSE CONNECTION
# ============================================================

cursor.close()
conn.close()

print("\n🔌 PostgreSQL connection closed.")
print("✅ FlowChain ETL pipeline finished.")