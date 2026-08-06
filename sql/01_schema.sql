-- ==========================================
-- FlowChain Database Schema
-- ==========================================

CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(150) NOT NULL,
    Brand VARCHAR(100),
    CategoryID INT,
    UnitCost DECIMAL(10,2),
    SellingPrice DECIMAL(10,2),

    CONSTRAINT fk_category
        FOREIGN KEY(CategoryID)
        REFERENCES Categories(CategoryID)
);

CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY,
    SupplierName VARCHAR(150) NOT NULL,
    ContactPerson VARCHAR(100),
    Email VARCHAR(150),
    Phone VARCHAR(20),
    City VARCHAR(100),
    Country VARCHAR(100)
);

CREATE TABLE PurchaseOrders (
    PurchaseOrderID INT PRIMARY KEY,
    SupplierID INT,
    OrderDate DATE,
    ExpectedDelivery DATE,
    Status VARCHAR(30),

    FOREIGN KEY (SupplierID)
        REFERENCES Suppliers(SupplierID)
);

CREATE TABLE PurchaseOrderItems (
    POItemID INT PRIMARY KEY,
    PurchaseOrderID INT,
    ProductID INT,
    Quantity INT,
    UnitPrice DECIMAL(10,2),

    FOREIGN KEY (PurchaseOrderID)
        REFERENCES PurchaseOrders(PurchaseOrderID),

    FOREIGN KEY (ProductID)
        REFERENCES Products(ProductID)
);

CREATE TABLE Warehouses (
    WarehouseID INT PRIMARY KEY,
    WarehouseName VARCHAR(150),
    City VARCHAR(100),
    State VARCHAR(100),
    Capacity INT,
    Manager VARCHAR(100)
);

CREATE TABLE Inventory (
    InventoryID INT PRIMARY KEY,
    ProductID INT,
    WarehouseID INT,
    CurrentStock INT,
    ReorderLevel INT,

    FOREIGN KEY(ProductID)
        REFERENCES Products(ProductID),

    FOREIGN KEY(WarehouseID)
        REFERENCES Warehouses(WarehouseID)
);