# FlowChain Dataset

## Primary Dataset

FlowChain uses a public Kaggle supply-chain inventory dataset containing daily SKU-level operational data.

### Dataset Characteristics

- 91,250 records
- 15 original columns
- 50 SKUs
- 5 warehouses
- 10 suppliers
- 4 regions
- One year of daily data
- Sales and inventory information
- Supplier lead times
- Reorder points and quantities
- Unit cost and selling price
- Promotion indicators
- Demand forecasts

## Dataset Pipeline

```text
Raw Kaggle Dataset
        ↓
Python Inspection
        ↓
Exploratory Data Analysis
        ↓
Data Cleaning
        ↓
Feature Engineering
        ↓
Cleaned Dataset
        ↓
PostgreSQL
```
