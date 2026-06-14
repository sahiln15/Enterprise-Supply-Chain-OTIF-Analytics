import datetime
import random
import pandas as pd
from faker import Faker

# Initialize Faker and set seed for reproducibility
fake = Faker()
Faker.seed(42)
random.seed(42)

# Configuration: Adjust number of rows here
TOTAL_ORDERS = 500000

print(f"--- Starting Data Generation for {TOTAL_ORDERS} rows ---")

# ==========================================
# 1. GENERATE DIMENSION TABLES
# ==========================================

# Dim_Customers
customers_data = [
    {"Customer_ID": 101, "Customer_Name": "Walmart", "OTIF_Threshold": 0.95, "Penalty_Rate": 0.03},
    {"Customer_ID": 102, "Customer_Name": "Target", "OTIF_Threshold": 0.92, "Penalty_Rate": 0.025},
    {"Customer_ID": 103, "Customer_Name": "Costco", "OTIF_Threshold": 0.90, "Penalty_Rate": 0.04},
    {"Customer_ID": 104, "Customer_Name": "Amazon Retail", "OTIF_Threshold": 0.98, "Penalty_Rate": 0.05},
    {"Customer_ID": 105, "Customer_Name": "Home Depot", "OTIF_Threshold": 0.88, "Penalty_Rate": 0.02}
]
df_customers = pd.DataFrame(customers_data)

# Dim_Carriers
carriers_data = [
    {"Carrier_ID": 501, "Carrier_Name": "Swift Logistics", "Base_Cost_Per_Unit": 1.20},
    {"Carrier_ID": 502, "Carrier_Name": "FastFreight Co", "Base_Cost_Per_Unit": 2.10},
    {"Carrier_ID": 503, "Carrier_Name": "Global Express", "Base_Cost_Per_Unit": 3.50},
    {"Carrier_ID": 504, "Carrier_Name": "Interstate Trucking", "Base_Cost_Per_Unit": 1.05}
]
df_carriers = pd.DataFrame(carriers_data)

# Dim_Products
categories = ["Electronics", "Home Goods", "Automotive", "Apparel", "Toys"]
products_data = []
for i in range(1, 101):  # 100 unique products
    cat = random.choice(categories)
    unit_cost = round(random.uniform(5.0, 150.0), 2)
    unit_price = round(unit_cost * random.uniform(1.3, 2.0), 2)
    products_data.append({
        "Product_ID": f"PROD-{i:03d}",
        "Product_Name": f"{cat} Item #{i}",
        "Category": cat,
        "Unit_Cost": unit_cost,
        "Unit_Price": unit_price
    })
df_products = pd.DataFrame(products_data)

# ==========================================
# 2. GENERATE FACT_ORDERS TABLE
# ==========================================
orders_list = []
start_date = datetime.date(2024, 1, 1)

print("Generating Fact_Orders table (this might take a few moments)...")

for i in range(1, TOTAL_ORDERS + 1):
    order_id = f"ORD-{i:07d}"
    
    # Randomly pick dimensions
    cust = random.choice(customers_data)
    prod = random.choice(products_data)
    carr = random.choice(carriers_data)
    
    # Quantities (simulating order sizing)
    ordered_qty = random.randint(10, 500)
    
    # Introduce "In-Full" errors (3% chance of damaged or partial delivery)
    if random.random() < 0.03:
        delivered_qty = int(ordered_qty * random.uniform(0.70, 0.95))
    else:
        delivered_qty = ordered_qty
        
    # Timeline Logic
    order_date = start_date + datetime.timedelta(days=random.randint(0, 700))
    promised_days = random.choice([3, 5, 7])
    promised_date = order_date + datetime.timedelta(days=promised_days)
    
    # Determine shipping speed bottlenecks based on engineered flaws
    # Flaw: FastFreight shipping to Walmart is frequently bottlenecked
    if cust["Customer_Name"] == "Walmart" and carr["Carrier_Name"] == "FastFreight Co":
        delay_chance = 0.25  # 25% late rate
    else:
        delay_chance = 0.06  # Standard 6% industry delay rate
        
    if random.random() < delay_chance:
        # Late delivery
        actual_days = promised_days + random.randint(1, 6)
    else:
        # On-Time delivery
        actual_days = promised_days - random.randint(0, 2)
        
    actual_arrival_date = order_date + datetime.timedelta(days=actual_days)
    
    # Calculate carrier shipping costs based on distance factors
    shipping_cost = round(ordered_qty * carr["Base_Cost_Per_Unit"] * random.uniform(0.9, 1.1), 2)

    orders_list.append({
        "Order_ID": order_id,
        "Order_Date": order_date,
        "Promised_Date": promised_date,
        "Actual_Arrival_Date": actual_arrival_date,
        "Customer_ID": cust["Customer_ID"],
        "Product_ID": prod["Product_ID"],
        "Carrier_ID": carr["Carrier_ID"],
        "Ordered_Qty": ordered_qty,
        "Delivered_Qty": delivered_qty,
        "Shipping_Cost": shipping_cost
    })

df_orders = pd.DataFrame(orders_list)

# ==========================================
# 3. EXPORT TO CSV
# ==========================================
print("Exporting data tables to CSV files...")
df_customers.to_csv("Dim_Customers.csv", index=False)
df_carriers.to_csv("Dim_Carriers.csv", index=False)
df_products.to_csv("Dim_Products.csv", index=False)
df_orders.to_csv("Fact_Orders.csv", index=False)

print("--- Data Generation Complete! Files are saved in your folder. ---")
