-- ==========================================================
-- FlowChain
-- Business Analytics Queries
-- ==========================================================

-- ==========================================================
-- Query 1
-- List all products with their categories
-- ==========================================================

SELECT
    p.ProductID,
    p.ProductName,
    p.Brand,
    c.CategoryName,
    p.UnitCost,
    p.SellingPrice
FROM Products p
JOIN Categories c
ON p.CategoryID = c.CategoryID;





-- ==========================================================
-- Query 2
-- List all purchase orders with supplier names
-- ==========================================================

SELECT
    po.PurchaseOrderID,
    s.SupplierName,
    po.OrderDate,
    po.ExpectedDelivery,
    po.Status
FROM PurchaseOrders po
JOIN Suppliers s
ON po.SupplierID = s.SupplierID;





-- ==========================================================
-- Query 3
-- Display purchase order details
-- ==========================================================

SELECT
    po.PurchaseOrderID,
    s.SupplierName,
    p.ProductName,
    poi.Quantity,
    poi.UnitPrice
FROM PurchaseOrders po
JOIN Suppliers s
ON po.SupplierID = s.SupplierID
JOIN PurchaseOrderItems poi
ON po.PurchaseOrderID = poi.PurchaseOrderID
JOIN Products p
ON poi.ProductID = p.ProductID;





-- ==========================================================
-- Query 4
-- View warehouse inventory
-- ==========================================================

SELECT
    p.ProductName,
    w.WarehouseName,
    i.CurrentStock
FROM Inventory i
JOIN Products p
ON i.ProductID = p.ProductID
JOIN Warehouses w
ON i.WarehouseID = w.WarehouseID;





-- ==========================================================
-- Query 5
-- Products below reorder level
-- ==========================================================

SELECT
    p.ProductName,
    i.CurrentStock,
    i.ReorderLevel
FROM Inventory i
JOIN Products p
ON i.ProductID = p.ProductID
WHERE i.CurrentStock <= i.ReorderLevel;





-- ==========================================================
-- Query 6
-- Total products in each category
-- ==========================================================

SELECT
    c.CategoryName,
    COUNT(*) AS TotalProducts
FROM Products p
JOIN Categories c
ON p.CategoryID = c.CategoryID
GROUP BY c.CategoryName
ORDER BY TotalProducts DESC;





-- ==========================================================
-- Query 7
-- Average selling price by category
-- ==========================================================

SELECT
    c.CategoryName,
    ROUND(AVG(p.SellingPrice),2) AS AverageSellingPrice
FROM Products p
JOIN Categories c
ON p.CategoryID = c.CategoryID
GROUP BY c.CategoryName;





-- ==========================================================
-- Query 8
-- Total inventory available for each product
-- ==========================================================

SELECT
    p.ProductName,
    SUM(i.CurrentStock) AS TotalStock
FROM Inventory i
JOIN Products p
ON i.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY TotalStock DESC;





-- ==========================================================
-- Query 9
-- Total purchase value by supplier
-- ==========================================================

SELECT
    s.SupplierName,
    SUM(poi.Quantity * poi.UnitPrice) AS TotalPurchaseValue
FROM Suppliers s
JOIN PurchaseOrders po
ON s.SupplierID = po.SupplierID
JOIN PurchaseOrderItems poi
ON po.PurchaseOrderID = poi.PurchaseOrderID
GROUP BY s.SupplierName
ORDER BY TotalPurchaseValue DESC;





-- ==========================================================
-- Query 10
-- Highest priced product
-- ==========================================================

SELECT
    ProductName,
    SellingPrice
FROM Products
ORDER BY SellingPrice DESC
LIMIT 1;