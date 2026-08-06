# Data Dictionary

## Overview

The FlowChain database follows a normalized relational database design to support procurement, inventory, warehouse, logistics, supplier analytics, and AI-driven decision support.

The database consists of three categories of tables:

- Master Tables
- Transaction Tables
- Analytics Tables

---

# Master Tables

1. Categories
2. Products
3. Suppliers
4. Warehouses
5. Customers
6. Employees
7. Transport Partners

---

# Transaction Tables

8. Purchase Orders
9. Purchase Order Items
10. Inventory
11. Shipments
12. Shipment Items
13. Returns

---

# Analytics Tables

14. Supplier Performance

# Categories

## Purpose

Stores product categories used to classify products across the supply chain.

---

## Business Owner

Inventory Management

---

## Primary Key

CategoryID

---

## Relationships

One Category can have many Products.

Category (1) --------> (Many) Products

---

## Columns

| Column       | Data Type    | PK  | FK  | Nullable | Description                |
| ------------ | ------------ | --- | --- | -------- | -------------------------- |
| CategoryID   | INT          | ✅  | ❌  | ❌       | Unique category identifier |
| CategoryCode | VARCHAR(20)  | ❌  | ❌  | ❌       | Business category code     |
| CategoryName | VARCHAR(100) | ❌  | ❌  | ❌       | Category name              |
| Description  | TEXT         | ❌  | ❌  | ✅       | Category description       |
| Status       | VARCHAR(20)  | ❌  | ❌  | ❌       | Active / Inactive          |
| CreatedAt    | TIMESTAMP    | ❌  | ❌  | ❌       | Record creation time       |

---

## Business Rules

- CategoryID must be unique.
- CategoryCode must be unique.
- CategoryName cannot be duplicated.
- Every Product must belong to one Category.

---

## Sample Data

| CategoryID | CategoryCode | CategoryName |
| ---------- | ------------ | ------------ |
| 1          | CAT-001      | Laptops      |
| 2          | CAT-002      | Smartphones  |
| 3          | CAT-003      | Monitors     |
| 4          | CAT-004      | Accessories  |
