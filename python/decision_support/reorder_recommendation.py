import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "datasets" / "cleaned" / "supply_chain_cleaned.csv"

OUTPUT_DIR = BASE_DIR / "datasets" / "decision_support"
OUTPUT_FILE = OUTPUT_DIR / "reorder_recommendations.csv"


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------

def load_data():
    """Load the cleaned FlowChain supply-chain dataset."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {INPUT_FILE}"
        )

    return pd.read_csv(INPUT_FILE)


# ---------------------------------------------------------
# Recommendation logic
# ---------------------------------------------------------

def generate_recommendation(row):
    """
    Generate an explainable inventory recommendation
    using inventory level, reorder point, demand forecast,
    lead time, and existing supply-chain indicators.
    """

    inventory = row["Inventory_Level"]
    reorder_point = row["Reorder_Point"]
    forecast = row["Demand_Forecast"]
    lead_time = row["Supplier_Lead_Time_Days"]

    low_stock = row["Low_Stock_Flag"]
    stockout = row["Stockout_Flag"]
    replenishment = row["Replenishment_Flag"]

    # High-risk stockout condition
    if stockout == 1:
        return pd.Series(
            [
                "HIGH",
                "URGENT REORDER",
                "Current inventory has reached a stockout condition."
            ]
        )

    # Inventory below reorder point and forecast demand
    # is higher than available inventory
    if inventory < reorder_point and forecast > inventory:

        if lead_time >= 10:
            return pd.Series(
                [
                    "HIGH",
                    "PRIORITY REORDER",
                    "Inventory is below the reorder point, forecast demand "
                    "exceeds current inventory, and supplier lead time is high."
                ]
            )

        return pd.Series(
            [
                "MEDIUM",
                "REORDER",
                "Inventory is below the reorder point and forecast demand "
                "exceeds current inventory."
            ]
        )

    # Low stock but forecast demand is not above inventory
    if low_stock == 1:

        return pd.Series(
            [
                "MEDIUM",
                "MONITOR",
                "Inventory is below the recommended stock threshold."
            ]
        )

    # Existing replenishment signal
    if replenishment == 1:

        return pd.Series(
            [
                "MEDIUM",
                "MONITOR",
                "A replenishment signal is already present for this item."
            ]
        )

    # Long lead time with relatively lower inventory
    if lead_time >= 10 and inventory <= reorder_point * 1.25:

        return pd.Series(
            [
                "MEDIUM",
                "MONITOR",
                "Supplier lead time is high and inventory is close "
                "to the reorder point."
            ]
        )

    # Normal situation
    return pd.Series(
        [
            "LOW",
            "NO ACTION",
            "Inventory is currently above the reorder threshold "
            "with sufficient forecast coverage."
        ]
    )


# ---------------------------------------------------------
# Main processing
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("FlowChain - Inventory Reorder Recommendation Engine")
    print("=" * 60)

    # Load data
    df = load_data()

    print(f"\nDataset loaded successfully.")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    # Generate recommendations
    print("\nGenerating recommendations...")

    recommendations = df.apply(
        generate_recommendation,
        axis=1
    )

    recommendations.columns = [
        "Risk_Level",
        "Recommendation",
        "Recommendation_Reason"
    ]

    # Combine original data with recommendations
    result = pd.concat(
        [
            df,
            recommendations
        ],
        axis=1
    )

    # Create output directory
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save results
    result.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nRecommendation engine completed successfully.")

    print(f"\nOutput file:")
    print(OUTPUT_FILE)

    # Summary
    print("\nRecommendation Summary:")
    print(
        result["Recommendation"]
        .value_counts()
        .to_string()
    )

    print("\nRisk Summary:")
    print(
        result["Risk_Level"]
        .value_counts()
        .to_string()
    )

    print("\nSample Recommendations:")
    print(
        result[
            [
                "SKU_ID",
                "Warehouse_ID",
                "Inventory_Level",
                "Reorder_Point",
                "Demand_Forecast",
                "Supplier_Lead_Time_Days",
                "Risk_Level",
                "Recommendation"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()