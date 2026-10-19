import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
rows = 100
start_date = datetime(2026, 1, 1)

products = [f"PROD-{i:03d}" for i in range(1, 21)]
prod_mapping = {
    f"PROD-{i:03d}": {
        "Name": f"Product {chr(65 + (i % 10))}{i}",
        "Category": "Electronics" if i <= 7 else "Industrial" if i <= 14 else "Automotive"
    } for i in range(1, 21)
}

suppliers = ["Apex Logistics", "Nexus Global", "Titan Industries", "Vertex Supply Chain", "Beacon Corp"]
warehouses = ["WH-North (Chicago)", "WH-South (Dallas)", "WH-East (NJ)", "WH-West (LA)"]
regions = ["North America", "EMEA", "APAC", "LATAM"]

data = []
for i in range(rows):
    current_date = start_date + timedelta(days=int(i * 2.5))
    prod_id = np.random.choice(products)
    p_info = prod_mapping[prod_id]
    
    opening_stock = int(np.random.randint(500, 5000))
    incoming_stock = int(np.random.choice([0, 500, 1000, 1500, 2000], p=[0.3, 0.2, 0.2, 0.2, 0.1]))
    
    demand_forecast = int(np.random.randint(400, 2500))
    actual_demand = int(demand_forecast * np.random.uniform(0.75, 1.25))
    units_sold = min(opening_stock + incoming_stock, actual_demand)
    
    closing_stock = (opening_stock + incoming_stock) - units_sold
    reorder_level = int(demand_forecast * 0.4)
    reorder_status = "Trigger Reorder" if closing_stock <= reorder_level else "Stable"
    
    base_lead = np.random.randint(3, 15)
    delivery_delay = np.random.choice([0, 1, 2, 3, 5], p=[0.7, 0.1, 0.08, 0.07, 0.05])
    delivery_time = base_lead + delivery_delay
    delivery_status = "On Time" if delivery_delay == 0 else "Delayed"
    
    holding_cost_per_unit = round(np.random.uniform(1.50, 6.00), 2)
    inventory_holding_cost = round(closing_stock * holding_cost_per_unit, 2)
    stockout_status = "Yes" if actual_demand > (opening_stock + incoming_stock) else "No"
    
    forecast_accuracy = round(1 - (abs(demand_forecast - actual_demand) / demand_forecast), 4)
    forecast_accuracy = max(0.0, forecast_accuracy)
    
    cogs_proxy = units_sold * 15
    avg_inv_proxy = max(((opening_stock + closing_stock) / 2) * 15, 1)
    inventory_turnover = round(cogs_proxy / avg_inv_proxy, 2)

    data.append({
        "Date": current_date.strftime("%Y-%m-%d"),
        "Month": current_date.strftime("%B"),
        "Quarter": f"Q{(current_date.month - 1) // 3 + 1}",
        "Year": current_date.year,
        "Product ID": prod_id,
        "Product Name": p_info["Name"],
        "Product Category": p_info["Category"],
        "Supplier Name": np.random.choice(suppliers),
        "Warehouse Location": np.random.choice(warehouses),
        "Region": np.random.choice(regions),
        "Opening Stock": opening_stock,
        "Incoming Stock": incoming_stock,
        "Units Sold": units_sold,
        "Closing Stock": closing_stock,
        "Reorder Level": reorder_level,
        "Reorder Status": reorder_status,
        "Lead Time (Days)": base_lead,
        "Order Quantity": int(reorder_level * 1.5),
        "Delivery Status": delivery_status,
        "Delivery Time (Days)": delivery_time,
        "Inventory Holding Cost": inventory_holding_cost,
        "Stockout Status": stockout_status,
        "Demand Forecast": demand_forecast,
        "Actual Demand": actual_demand,
        "Forecast Accuracy %": forecast_accuracy,
        "Inventory Turnover Ratio": inventory_turnover
    })

df = pd.DataFrame(data)
df.to_csv("supply_chain_data.csv", index=False)
print("Data generation complete!")
