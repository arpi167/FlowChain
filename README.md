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

FlowChain is designed to use Excel and Power BI to convert database results into business dashboards.

### Planned KPIs

- Total Products
- Total Suppliers
- Total Inventory
- Low Stock Products
- Pending Purchase Orders
- Procurement Value
- Supplier Performance
- Warehouse Stock Distribution

### Dashboard Areas

#### Inventory Overview

- Current stock levels
- Reorder alerts
- Warehouse distribution
- Stock availability

#### Procurement Overview

- Purchase order volume
- Pending orders
- Order status
- Procurement value

#### Supplier Analysis

- Supplier order volume
- Supplier contribution
- Delivery performance
- Procurement value

---

## 🤖 Decision Support

FlowChain is designed to extend traditional analytics into decision-support capabilities.

Planned capabilities include:

- Inventory reorder recommendations
- Supplier performance analysis
- Demand forecasting
- Procurement risk detection
- Stock-out risk identification

These features will be developed incrementally after the core analytics layer is completed.

---

## 🐍 Python Analytics

Python will be used for data preparation, analysis, and advanced analytics.

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
│
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
│
├── powerbi/
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

### In Progress

- [ ] Dataset preparation
- [ ] Python exploratory data analysis
- [ ] Excel analytics
- [ ] Power BI dashboard
- [ ] Supplier performance analytics
- [ ] Inventory analytics
- [ ] Decision-support features

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
- Power BI
- Excel Analytics
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
- Planned KPI-driven dashboards using Power BI and Excel.
- Designed a roadmap for predictive and AI-assisted supply chain decision support.
- Applied documentation and version-control practices using Git and GitHub.

---

## 🚀 Future Enhancements

Future versions of FlowChain may include:

- Automated inventory reorder recommendations
- Demand forecasting
- Supplier performance scoring
- Procurement risk detection
- Stock-out prediction
- Interactive Power BI dashboards
- Automated analytical reports
- Machine learning-based decision support

---

## 👩‍💻 Author

**Arpita Bhat**

B.E. Computer Science & Engineering (Data Science)

Interested in Data Science, Machine Learning, Business Analytics, and AI.

---

## 📌 Disclaimer

FlowChain is a student-built portfolio project created using generated business data and public dataset concepts for educational and demonstration purposes.
