import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. Load Dataset
# --------------------------------------------------

DATA_DIR = Path(__file__).resolve().parents[2] / "datasets" / "raw"

csv_files = list(DATA_DIR.glob("*.csv"))

if not csv_files:
    print("❌ No CSV file found in datasets/raw/")
    raise SystemExit

dataset_path = csv_files[0]

df = pd.read_csv(dataset_path)

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

print("=" * 70)
print("FLOWCHAIN - EXPLORATORY DATA ANALYSIS")
print("=" * 70)

# --------------------------------------------------
# 2. Basic Dataset Information
# --------------------------------------------------

print("\n📊 DATASET OVERVIEW")

print(f"Rows           : {len(df):,}")
print(f"Columns        : {len(df.columns)}")
print(f"Date Range     : {df['Date'].min().date()} to {df['Date'].max().date()}")
print(f"Unique SKUs    : {df['SKU_ID'].nunique()}")
print(f"Warehouses     : {df['Warehouse_ID'].nunique()}")
print(f"Suppliers      : {df['Supplier_ID'].nunique()}")
print(f"Regions        : {df['Region'].nunique()}")

# --------------------------------------------------
# 3. Unique Values
# --------------------------------------------------

print("\n📦 UNIQUE VALUES")

print("\nSKUs:")
print(df["SKU_ID"].unique())

print("\nWarehouses:")
print(df["Warehouse_ID"].unique())

print("\nSuppliers:")
print(df["Supplier_ID"].unique())

print("\nRegions:")
print(df["Region"].unique())

# --------------------------------------------------
# 4. Sales Analysis
# --------------------------------------------------

print("\n💰 SALES ANALYSIS")

total_units_sold = df["Units_Sold"].sum()

print(f"Total Units Sold : {total_units_sold:,}")
print(f"Average Daily Units Sold : {df['Units_Sold'].mean():.2f}")

# Top SKUs by sales
top_skus = (
    df.groupby("SKU_ID")["Units_Sold"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 SKUs by Units Sold:")
print(top_skus)

# --------------------------------------------------
# 5. Warehouse Analysis
# --------------------------------------------------

print("\n🏭 WAREHOUSE ANALYSIS")

warehouse_sales = (
    df.groupby("Warehouse_ID")["Units_Sold"]
    .sum()
    .sort_values(ascending=False)
)

print("\nUnits Sold by Warehouse:")
print(warehouse_sales)

warehouse_inventory = (
    df.groupby("Warehouse_ID")["Inventory_Level"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Inventory by Warehouse:")
print(warehouse_inventory.round(2))

# --------------------------------------------------
# 6. Supplier Analysis
# --------------------------------------------------

print("\n🚚 SUPPLIER ANALYSIS")

supplier_summary = df.groupby("Supplier_ID").agg(
    Total_Units_Sold=("Units_Sold", "sum"),
    Average_Lead_Time=("Supplier_Lead_Time_Days", "mean"),
    Product_Count=("SKU_ID", "nunique")
)

supplier_summary = supplier_summary.sort_values(
    "Total_Units_Sold",
    ascending=False
)

print(supplier_summary.round(2))

# --------------------------------------------------
# 7. Regional Analysis
# --------------------------------------------------

print("\n🌍 REGIONAL ANALYSIS")

region_sales = (
    df.groupby("Region")["Units_Sold"]
    .sum()
    .sort_values(ascending=False)
)

print("\nUnits Sold by Region:")
print(region_sales)

# --------------------------------------------------
# 8. Inventory & Reorder Analysis
# --------------------------------------------------

print("\n📦 INVENTORY ANALYSIS")

low_stock = df[df["Inventory_Level"] <= df["Reorder_Point"]]

print(f"Low Stock Records : {len(low_stock):,}")

print(
    f"Low Stock Percentage : "
    f"{len(low_stock) / len(df) * 100:.2f}%"
)

# --------------------------------------------------
# 9. Replenishment Analysis
# --------------------------------------------------

print("\n🔄 REPLENISHMENT ANALYSIS")

orders = df[df["Order_Quantity"] > 0]

print(f"Records with Replenishment Orders : {len(orders):,}")

print(
    f"Total Replenishment Quantity : "
    f"{df['Order_Quantity'].sum():,}"
)

print(
    f"Average Order Quantity "
    f"(when order exists) : "
    f"{orders['Order_Quantity'].mean():.2f}"
)

# --------------------------------------------------
# 10. Revenue and Profit Analysis
# --------------------------------------------------

print("\n💵 REVENUE & PROFIT ANALYSIS")

df["Revenue"] = df["Units_Sold"] * df["Unit_Price"]

df["Cost"] = df["Units_Sold"] * df["Unit_Cost"]

df["Profit"] = df["Revenue"] - df["Cost"]

print(f"Total Revenue : ${df['Revenue'].sum():,.2f}")
print(f"Total Cost    : ${df['Cost'].sum():,.2f}")
print(f"Total Profit  : ${df['Profit'].sum():,.2f}")

profit_margin = (
    df["Profit"].sum() /
    df["Revenue"].sum()
) * 100

print(f"Profit Margin : {profit_margin:.2f}%")

# --------------------------------------------------
# 11. Promotion Analysis
# --------------------------------------------------

print("\n🎯 PROMOTION ANALYSIS")

promotion_rate = df["Promotion_Flag"].mean() * 100

print(f"Promotion Rate : {promotion_rate:.2f}%")

promotion_sales = df.groupby("Promotion_Flag")["Units_Sold"].mean()

print("\nAverage Units Sold:")
print(promotion_sales)

# --------------------------------------------------
# 12. Demand Forecast Analysis
# --------------------------------------------------

print("\n🔮 DEMAND FORECAST ANALYSIS")

df["Forecast_Error"] = (
    df["Units_Sold"] - df["Demand_Forecast"]
)

df["Absolute_Forecast_Error"] = (
    df["Forecast_Error"].abs()
)

mae = df["Absolute_Forecast_Error"].mean()

print(f"Mean Absolute Error (MAE) : {mae:.2f}")

# --------------------------------------------------
# 13. Stockout Investigation
# --------------------------------------------------

print("\n⚠️ STOCKOUT ANALYSIS")

stockout_count = df["Stockout_Flag"].sum()

print(f"Stockout Records : {stockout_count:,}")

if stockout_count == 0:
    print(
        "⚠️ Stockout_Flag contains only 0 values. "
        "The dataset does not contain recorded stockout events."
    )

# --------------------------------------------------
# 14. Reorder Point Analysis
# --------------------------------------------------

print("\n📋 REORDER ANALYSIS")

reorder_records = df[
    df["Inventory_Level"] <= df["Reorder_Point"]
]

print(
    f"Records at or below reorder point : "
    f"{len(reorder_records):,}"
)

# --------------------------------------------------
# 15. Final Summary
# --------------------------------------------------

print("\n" + "=" * 70)
print("EDA COMPLETE")
print("=" * 70)