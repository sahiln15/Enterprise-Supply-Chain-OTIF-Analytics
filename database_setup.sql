-- 1. Create Customer Dimension Table
CREATE TABLE Dim_Customers (
    Customer_ID INT PRIMARY KEY,
    Customer_Name VARCHAR(100),
    OTIF_Threshold DECIMAL(4,3),
    Penalty_Rate DECIMAL(4,3)
);

-- 2. Create Carrier Dimension Table
CREATE TABLE Dim_Carriers (
    Carrier_ID INT PRIMARY KEY,
    Carrier_Name VARCHAR(100),
    Base_Cost_Per_Unit DECIMAL(10,2)
);

-- 3. Create Product Dimension Table
CREATE TABLE Dim_Products (
    Product_ID VARCHAR(50) PRIMARY KEY,
    Product_Name VARCHAR(150),
    Category VARCHAR(100),
    Unit_Cost DECIMAL(10,2),
    Unit_Price DECIMAL(10,2)
);

-- 4. Create Fact Orders Table with Foreign Keys
CREATE TABLE Fact_Orders (
    Order_ID VARCHAR(50) PRIMARY KEY,
    Order_Date DATE,
    Promised_Date DATE,
    Actual_Arrival_Date DATE,
    Customer_ID INT,
    Product_ID VARCHAR(50),
    Carrier_ID INT,
    Ordered_Qty INT,
    Delivered_Qty INT,
    Shipping_Cost DECIMAL(10,2),
    FOREIGN KEY (Customer_ID) REFERENCES Dim_Customers(Customer_ID),
    FOREIGN KEY (Product_ID) REFERENCES Dim_Products(Product_ID),
    FOREIGN KEY (Carrier_ID) REFERENCES Dim_Carriers(Carrier_ID)
);

SELECT COUNT(*) FROM Fact_Orders;

