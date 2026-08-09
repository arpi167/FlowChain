import pandas as pd
from pathlib import Path

# ============================================================
# FLOWCHAIN - DATA CLEANING & FEATURE ENGINEERING
# ============================================================

# ------------------------------------------------------------
# 1. Define paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "datasets" / "raw"
CLEANED_DIR = PROJECT_ROOT / "datasets" / "cleaned"

CLEANED_DIR.mkdir(parents=True, exist_ok=True)

# Find raw CSV
csv_files = list(RAW_DIR.glob("*.csv"))

if not csv_files:
    print("❌ No CSV dataset found in datasets/raw/")
    raise SystemExit

input_file = csv_files[0]
output_file = CLEANED_DIR / "supply_chain_cleaned.csv"

print("=" * 70)
print("FLOWCHAIN - DATA CLEANING")
print("=" * 70)

print(f"\n📂 Input file:")
print(input_file)

# ------------------------------------------------------------
# 2. Load dataset
# ------------------------------------------------------------

df = pd.read_csv(input_file)

print(f"\nOriginal rows    : {len(df):,}")
print(f"Original columns : {len(df.columns)}")

# ------------------------------------------------------------
# 3. Standardize column names
# ------------------------------------------------------------

df.columns = df.columns.str.strip()

print("\n✅ Column names standardized")

# ------------------------------------------------------------
# 4. Convert Date column
# ------------------------------------------------------------

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Check invalid dates
invalid_dates = df["Date"].isna().sum()

print(f"\nInvalid dates : {invalid_dates}")

# ------------------------------------------------------------
# 5. Remove duplicate rows
# ------------------------------------------------------------

duplicates_before = df.duplicated().sum()

print(f"Duplicate rows found : {duplicates_before}")

if duplicates_before > 0:
    df = df.drop_duplicates()

print(f"Rows after duplicate removal : {len(df):,}")

# ------------------------------------------------------------
# 6. Handle missing values
# ------------------------------------------------------------

missing_before = df.isnull().sum().sum()

print(f"\nMissing values before cleaning : {missing_before}")

# Numeric columns
numeric_columns = [
    "Units_Sold",
    "Inventory_Level",
    "Supplier_Lead_Time_Days",
    "Reorder_Point",
    "Order_Quantity",
    "Unit_Cost",
    "Unit_Price",
    "Promotion_Flag",
    "Stockout_Flag",
    "Demand_Forecast"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

# Remove rows with missing critical values
critical_columns = [
    "Date",
    "SKU_ID",
    "Warehouse_ID",
    "Supplier_ID",
    "Region"
]

df = df.dropna(subset=critical_columns)

# Fill missing numeric values using median
for column in numeric_columns:
    if column in df.columns:
        df[column] = df[column].fillna(df[column].median())

missing_after = df.isnull().sum().sum()

print(f"Missing values after cleaning  : {missing_after}")

# ------------------------------------------------------------
# 7. Validate non-negative business values
# ------------------------------------------------------------

non_negative_columns = [
    "Units_Sold",
    "Inventory_Level",
    "Reorder_Point",
    "Order_Quantity",
    "Unit_Cost",
    "Unit_Price",
    "Demand_Forecast"
]

for column in non_negative_columns:
    if column in df.columns:
        df.loc[df[column] < 0, column] = 0

# Lead time must be positive
df.loc[df["Supplier_Lead_Time_Days"] <= 0, "Supplier_Lead_Time_Days"] = 1

# ------------------------------------------------------------
# 8. Validate binary flags
# ------------------------------------------------------------

df["Promotion_Flag"] = df["Promotion_Flag"].astype(int)
df["Stockout_Flag"] = df["Stockout_Flag"].astype(int)

# Keep flags strictly 0 or 1
df["Promotion_Flag"] = df["Promotion_Flag"].clip(0, 1)
df["Stockout_Flag"] = df["Stockout_Flag"].clip(0, 1)

# ------------------------------------------------------------
# 9. Feature Engineering
# ------------------------------------------------------------

print("\n🔧 Creating analytical features...")

# Revenue
df["Revenue"] = df["Units_Sold"] * df["Unit_Price"]

# Cost
df["Cost"] = df["Units_Sold"] * df["Unit_Cost"]

# Profit
df["Profit"] = df["Revenue"] - df["Cost"]

# Profit margin
df["Profit_Margin"] = 0.0

revenue_positive = df["Revenue"] > 0

df.loc[revenue_positive, "Profit_Margin"] = (
    df.loc[revenue_positive, "Profit"]
    / df.loc[revenue_positive, "Revenue"]
) * 100

# Forecast error
df["Forecast_Error"] = (
    df["Units_Sold"] - df["Demand_Forecast"]
)

# Absolute forecast error
df["Absolute_Forecast_Error"] = (
    df["Forecast_Error"].abs()
)

# Low stock flag
df["Low_Stock_Flag"] = (
    df["Inventory_Level"] <= df["Reorder_Point"]
).astype(int)

# Replenishment flag
df["Replenishment_Flag"] = (
    df["Order_Quantity"] > 0
).astype(int)

# ------------------------------------------------------------
# 10. Sort dataset
# ------------------------------------------------------------

df = df.sort_values(
    by=["Date", "SKU_ID", "Warehouse_ID"]
).reset_index(drop=True)

# ------------------------------------------------------------
# 11. Round decimal columns
# ------------------------------------------------------------

decimal_columns = [
    "Unit_Cost",
    "Unit_Price",
    "Demand_Forecast",
    "Revenue",
    "Cost",
    "Profit",
    "Profit_Margin",
    "Forecast_Error",
    "Absolute_Forecast_Error"
]

for column in decimal_columns:
    if column in df.columns:
        df[column] = df[column].round(2)

# ------------------------------------------------------------
# 12. Final validation
# ------------------------------------------------------------

print("\n📊 FINAL VALIDATION")

print(f"Final rows    : {len(df):,}")
print(f"Final columns : {len(df.columns)}")

print(f"\nRemaining missing values : {df.isnull().sum().sum()}")
print(f"Remaining duplicates     : {df.duplicated().sum()}")

print(
    f"Low-stock records        : "
    f"{df['Low_Stock_Flag'].sum():,}"
)

print(
    f"Replenishment records    : "
    f"{df['Replenishment_Flag'].sum():,}"
)

print(
    f"Total revenue            : "
    f"${df['Revenue'].sum():,.2f}"
)

print(
    f"Total profit             : "
    f"${df['Profit'].sum():,.2f}"
)

# ------------------------------------------------------------
# 13. Save cleaned dataset
# ------------------------------------------------------------

df.to_csv(output_file, index=False)

print("\n💾 Cleaned dataset saved successfully!")

print(f"Output:")
print(output_file)

print("\n" + "=" * 70)
print("DATA CLEANING COMPLETE")
print("=" * 70)