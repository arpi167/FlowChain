import pandas as pd
from pathlib import Path

# Path to the raw dataset
DATA_DIR = Path(__file__).resolve().parents[2] / "datasets" / "raw"

# Find CSV files
csv_files = list(DATA_DIR.glob("*.csv"))

if not csv_files:
    print("❌ No CSV file found in datasets/raw/")
    print(f"Checked: {DATA_DIR}")
    raise SystemExit

print("📂 Dataset files found:")
for file in csv_files:
    print(f" - {file.name}")

# Use the first CSV file
dataset_path = csv_files[0]

print("\n📌 Loading dataset:")
print(dataset_path)

df = pd.read_csv(dataset_path)

print("\n" + "=" * 60)
print("FLOWCHAIN DATASET INSPECTION")
print("=" * 60)

# Basic information
print("\n📊 Dataset Shape")
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]:,}")

# Column names
print("\n📋 Columns")
for column in df.columns:
    print(f" - {column}")

# Data types
print("\n🔤 Data Types")
print(df.dtypes)

# Missing values
print("\n❓ Missing Values")
missing = df.isnull().sum()

for column, count in missing.items():
    print(f" - {column}: {count:,}")

# Duplicate rows
print("\n♻️ Duplicate Rows")
print(f"Duplicates: {df.duplicated().sum():,}")

# First 5 rows
print("\n👀 First 5 Rows")
print(df.head())

# Basic statistics
print("\n📈 Numerical Summary")
print(df.describe(include="all").transpose())

print("\n" + "=" * 60)
print("INSPECTION COMPLETE")
print("=" * 60)