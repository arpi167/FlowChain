# FlowChain — Supply Chain Analytics & Decision Support Platform

FlowChain is an end-to-end supply chain analytics project designed to help businesses monitor procurement, inventory, suppliers, and operational performance.

The project combines PostgreSQL, SQL, Python, Excel, and Power BI to transform business data into actionable insights and decision-support capabilities.

---

## 🎯 Project Objective

The objective of FlowChain is to build a centralized supply chain analytics system that can answer practical business questions such as:

- Which products are running low on stock?
- Which suppliers are performing well?
- Which purchase orders are pending or delayed?
- Which products require reordering?
- How is inventory distributed across warehouses?
- Which suppliers contribute the highest procurement value?
- What operational risks require attention?

The project follows a complete data workflow:

**Data → Database → SQL Analytics → BI → Decision Support**

---

## 🏗️ System Architecture

FlowChain follows a layered architecture:

```text
DATA SOURCES
      ↓
DATA PREPARATION
      ↓
POSTGRESQL DATABASE
      ↓
SQL ANALYTICS
      ↓
ANALYTICS & BI
      ↓
AI DECISION SUPPORT
      ↓
BUSINESS DECISIONS
```

### Architecture Components

| Layer               | Technology / Purpose                                                    |
| ------------------- | ----------------------------------------------------------------------- |
| Data Sources        | Kaggle, Public Datasets, Generated Business Data                        |
| Data Preparation    | Python, Pandas                                                          |
| Database            | PostgreSQL                                                              |
| SQL Analytics       | SQL, Joins, Aggregations, KPIs                                          |
| Analytics & BI      | Excel, Power BI, Python                                                 |
| AI Decision Support | Reorder Recommendations, Supplier Analysis, Forecasting, Risk Detection |
| Business Output     | Procurement, Inventory and Supplier Decisions                           |

Architecture diagram:

`docs/06_Architecture.drawio`

---

## 🗄️ Database Design

PostgreSQL is used as the central relational database for FlowChain.

### Core Tables

| Table              | Purpose                                                |
| ------------------ | ------------------------------------------------------ |
| Categories         | Stores product categories                              |
| Products           | Stores product information and category relationships  |
| Suppliers          | Stores supplier information                            |
| PurchaseOrders     | Stores purchase orders created for suppliers           |
| PurchaseOrderItems | Stores individual products included in purchase orders |
| Warehouses         | Stores warehouse information                           |
| Inventory          | Tracks product stock levels and reorder thresholds     |

---

## 🔗 Database Relationships

The main database relationships are:

```text
Categories 1 ───── N Products

Products 1 ───── N Inventory

Warehouses 1 ───── N Inventory

Products 1 ───── N PurchaseOrderItems

PurchaseOrders 1 ───── N PurchaseOrderItems

Suppliers 1 ───── N PurchaseOrders
```

The complete ER diagram is available at:

`docs/03_ER_Diagram.drawio`

---

## 📊 SQL Analytics

FlowChain includes business-oriented SQL queries designed to support operational analysis.

### Low Stock Detection

Identifies products whose current stock has reached or fallen below the reorder level.

```sql
SELECT
    p.ProductName,
    i.CurrentStock,
    i.ReorderLevel
FROM Inventory i
JOIN Products p
ON i.ProductID = p.ProductID
WHERE i.CurrentStock <= i.ReorderLevel;
```

This query helps identify products that may require replenishment.

### Other Analytics Areas

The SQL analytics layer supports:

- Inventory analysis
- Low-stock detection
- Procurement analysis
- Supplier analysis
- Purchase order tracking
- Warehouse stock analysis
- KPI generation
- Business reporting

SQL queries are stored in:

`sql/03_business_queries.sql`

---

## 📈 Analytics & Business Intelligence

FlowChain uses Microsoft Excel and Power BI to convert analytical results into business dashboards and decision-support views.

### Dashboard Files

| Dashboard                    | File                              |
| ---------------------------- | --------------------------------- |
| Excel Analytics Dashboard    | `excel/FlowChain_Analysis.xlsx`   |
| Power BI Analytics Dashboard | `powerbi/FlowChain_Analysis.pbix` |

### Power BI Dashboard Pages

The Power BI dashboard contains four analytical pages:

1. **Executive Supply Chain Dashboard**
2. **Sales & Profit Analysis**
3. **Inventory & Supply Chain**
4. **Demand Forecast**

---

## 📌 Key Performance Indicators

The dashboards include key supply-chain and business KPIs such as:

- Total Revenue
- Total Profit
- Total Units Sold
- Average Profit Margin
- Total Inventory
- Replenishment Orders
- Stockout Monitoring
- Average Forecast Error

---

## 📊 Dashboard Analysis

### Executive Supply Chain Dashboard

Provides a high-level overview of the supply-chain operation through KPI cards.

Key metrics include:

- Total Revenue
- Total Profit
- Total Units Sold
- Average Profit Margin
- Total Inventory
- Replenishment Orders
- Stockout Monitoring

### Sales & Profit Analysis

Analyzes business performance across warehouses, products, promotions, and regions.

Visualizations include:

- Warehouse Revenue vs Cost vs Profit
- Promotion vs Non-Promotion Sales
- Top 10 Most Profitable SKUs
- Revenue by Region

### Inventory & Supply Chain

Focuses on inventory levels, replenishment activity, stock availability, and reorder thresholds.

Visualizations include:

- Inventory by Warehouse
- Replenishment Orders by Warehouse
- Low Stock Analysis
- Inventory Level vs Reorder Point

### Demand Forecast

Provides forecasting-related analysis and forecast error monitoring.

Visualizations include:

- Forecast Demand Trend
- Top 10 SKUs by Forecast Error
- Forecast Error Trend
- Average Forecast Error

---

## 🤖 Decision Support

FlowChain is designed to extend traditional analytics into decision-support capabilities.

Planned capabilities include:

- Inventory reorder recommendations
- Supplier performance analysis
- Demand forecasting enhancements
- Procurement risk detection
- Stock-out risk identification
- AI-assisted decision support

These features will be developed incrementally after the core analytics layer is completed.

---

## 🐍 Python Analytics

Python is used for data preparation, analysis, and advanced analytics.

### Python Use Cases

- Data cleaning
- Data validation
- Exploratory Data Analysis
- Statistical analysis
- Forecasting
- Analytical automation

### Main Libraries

- Pandas
- NumPy
- Matplotlib
- Scikit-learn

---

## 🔄 Project Workflow

```text
1. Collect / Generate Data
            ↓
2. Clean & Validate Data
            ↓
3. Load Data into PostgreSQL
            ↓
4. Perform SQL Analysis
            ↓
5. Create Business KPIs
            ↓
6. Build Excel / Power BI Dashboards
            ↓
7. Develop Decision-Support Features
            ↓
8. Generate Business Insights
```

---

## 📂 Project Structure

```text
FlowChain/
│
├── assets/
├── datasets/
│
├── docs/
│   ├── 01_BRD.md
│   ├── 02_Data_Dictionary.md
│   ├── 03_ER_Diagram.drawio
│   ├── 04_Dataset_Strategy.md
│   ├── 05_Project_Roadmap.md
│   └── 06_Architecture.drawio
│
├── excel/
│   └── FlowChain_Analysis.xlsx
│
├── powerbi/
│   └── FlowChain_Analysis.pbix
│
├── python/
│
├── sql/
│   ├── 01_schema.sql
│   ├── 02_sample_data.sql
│   └── 03_business_queries.sql
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🛠️ Technology Stack

### Database

- PostgreSQL
- pgAdmin 4

### Programming & Data Analytics

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib

### Business Intelligence

- Microsoft Excel
- Power BI

### Documentation & Design

- Markdown
- Draw.io

### Version Control

- Git
- GitHub

---

## 📚 Project Documentation

| Document                 | Description                                 |
| ------------------------ | ------------------------------------------- |
| `01_BRD.md`              | Business Requirements Document              |
| `02_Data_Dictionary.md`  | Database table and field definitions        |
| `03_ER_Diagram.drawio`   | Entity Relationship Diagram                 |
| `04_Dataset_Strategy.md` | Dataset collection and preparation strategy |
| `05_Project_Roadmap.md`  | Project development roadmap                 |
| `06_Architecture.drawio` | End-to-end system architecture              |

---

## 📌 Current Project Status

### Completed

- [x] Business Requirements Document
- [x] Database design
- [x] PostgreSQL database setup
- [x] Core relational tables
- [x] Sample business data
- [x] SQL business queries
- [x] Entity Relationship Diagram
- [x] System Architecture Diagram
- [x] GitHub repository setup
- [x] Project documentation
- [x] Excel supply chain analytics dashboard
- [x] Power BI supply chain analytics dashboard
- [x] Executive KPI dashboard
- [x] Sales & Profit Analysis dashboard
- [x] Inventory & Supply Chain dashboard
- [x] Demand Forecast dashboard

### In Progress

- [ ] Advanced supplier performance analytics
- [ ] Automated inventory reorder recommendations
- [ ] Demand forecasting enhancements
- [ ] Procurement risk detection
- [ ] AI-assisted decision support

---

## 🎓 Skills Demonstrated

- Relational Database Design
- PostgreSQL
- SQL
- SQL Joins
- SQL Aggregations
- Business Analytics
- Data Cleaning
- Exploratory Data Analysis
- KPI Development
- Data Visualization
- Excel Dashboard Development
- Power BI Dashboard Development
- Supply Chain KPI Analysis
- Forecast Error Analysis
- Inventory & Replenishment Analytics
- Business Intelligence Reporting
- Python
- Git & GitHub
- Business Requirement Analysis
- System Architecture

---

## 💼 Resume-Relevant Highlights

FlowChain demonstrates an end-to-end analytics workflow rather than only database creation.

Key areas include:

- Designed a relational supply chain database using PostgreSQL with interconnected entities.
- Developed business-oriented SQL queries for inventory and procurement analysis.
- Designed an ER model and system architecture for a supply chain analytics platform.
- Built Excel and Power BI dashboards for supply-chain KPI and operational analysis.
- Created dashboard views covering sales, profitability, inventory, replenishment, stockout monitoring, and demand forecasting.
- Designed a roadmap for predictive and AI-assisted supply chain decision support.
- Applied documentation and version-control practices using Git and GitHub.

---

## 🚀 Future Enhancements

Future versions of FlowChain may include:

- Automated inventory reorder recommendations
- Advanced demand forecasting
- Supplier performance scoring
- Procurement risk detection
- Stock-out prediction
- Automated analytical reports
- Machine learning-based decision support
- AI-assisted supply chain recommendations

---

## 👩‍💻 Author

**Arpita Bhat**

B.E. Computer Science & Engineering (Data Science)

Interested in Data Science, Machine Learning, Business Analytics, and AI.

---

## 📌 Disclaimer

FlowChain is a student-built portfolio project created using generated business data and public dataset concepts for educational and demonstration purposes.
