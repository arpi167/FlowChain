-- ==========================================
-- FlowChain Sample Data
-- ==========================================

-- ==========================================
-- Categories
-- ==========================================

INSERT INTO Categories VALUES
(1,'Laptops'),
(2,'Smartphones'),
(3,'Monitors'),
(4,'Accessories'),
(5,'Printers');



-- ==========================================
-- Products
-- ==========================================

INSERT INTO Products VALUES
(101,'Dell Inspiron 15','Dell',1,42000,49999),
(102,'Samsung Galaxy S24','Samsung',2,58000,64999),
(103,'LG UltraFine 27','LG',3,11500,14999),
(104,'Logitech MX Master 3S','Logitech',4,4500,6999),
(105,'HP LaserJet MFP','HP',5,18500,23999);



-- ==========================================
-- Suppliers
-- ==========================================

INSERT INTO Suppliers VALUES
(1,'ABC Technologies','Rahul Sharma','rahul@abctech.com','9876543210','Bengaluru','India'),

(2,'Global Electronics','Priya Nair','priya@globalelectronics.com','9123456780','Mumbai','India'),

(3,'Tech World Pvt Ltd','Amit Verma','amit@techworld.com','9988776655','Delhi','India'),

(4,'Future Devices Ltd','Sneha Rao','sneha@futuredevices.com','9012345678','Hyderabad','India'),

(5,'Smart Components','Karan Patel','karan@smartcomponents.com','9090909090','Ahmedabad','India');



-- ==========================================
-- Purchase Orders
-- ==========================================

INSERT INTO PurchaseOrders VALUES
(1001,1,'2026-08-15','2026-08-20','Pending'),

(1002,2,'2026-08-16','2026-08-22','Delivered'),

(1003,3,'2026-08-18','2026-08-25','Pending');



-- ==========================================
-- Purchase Order Items
-- ==========================================

INSERT INTO PurchaseOrderItems VALUES
(1,1001,101,50,42000),

(2,1001,105,10,18500),

(3,1002,102,30,58000),

(4,1002,104,100,4500),

(5,1003,103,25,11500);



-- ==========================================
-- Warehouses
-- ==========================================

INSERT INTO Warehouses VALUES
(1,'Bangalore Central Warehouse','Bengaluru','Karnataka',10000,'Ravi Kumar'),

(2,'Mumbai Distribution Center','Mumbai','Maharashtra',8000,'Priya Shah'),

(3,'Delhi Storage Hub','Delhi','Delhi',12000,'Amit Gupta');



-- ==========================================
-- Inventory
-- ==========================================

INSERT INTO Inventory VALUES
(1,101,1,50,20),

(2,101,2,30,20),

(3,102,1,40,15),

(4,103,3,25,10),

(5,104,2,150,50),

(6,105,1,18,10);