# sales_dashboard.py
# Beginner project on sales performance dashboard using SQLite + Python

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("superstore.csv", encoding='latin1') # 1. Loading dataset

df['Order Date'] = pd.to_datetime(df['Order Date'])   # 2. Convert date column to proper datetime

conn = sqlite3.connect("sales.db")                    # 3. Create SQLite DB and store data         
df.to_sql("sales", conn, if_exists="replace", index=False)

# ---------------------- SQL QUERIES ----------------------

# Monthly Sales Trends
monthly_sales_query = """
SELECT strftime('%Y-%m', "Order Date") AS month, SUM(Sales) AS total_sales
FROM sales
GROUP BY month
ORDER BY month
"""
monthly_sales = pd.read_sql(monthly_sales_query, conn)

# Top 10 Products by Sales
top_products_query = """
SELECT "Product Name", SUM(Sales) AS total_sales
FROM sales
GROUP BY "Product Name"
ORDER BY total_sales DESC
LIMIT 10
"""
top_products = pd.read_sql(top_products_query, conn)

# Sales by Category
category_sales_query = """
SELECT Category, SUM(Sales) AS total_sales
FROM sales
GROUP BY Category
ORDER BY total_sales DESC
"""
category_sales = pd.read_sql(category_sales_query, conn)

# Simple Churn (customers who bought before 2017 excluding 2017)
query_b42017 = """
SELECT DISTINCT "Customer ID"
FROM sales
WHERE "Order Date" < '2017-01-01'
EXCEPT
SELECT DISTINCT "Customer ID"
FROM sales
WHERE "Order Date" >= '2017-01-01'
"""
cust_b42017 = pd.read_sql(query_b42017, conn)

print(f"Number of churned customers: {len(cust_b42017)}")

# ---------------------- VISUALIZATIONS ----------------------

sns.set_style("whitegrid")

# Monthly sales trend
plt.figure(figsize=(10, 5))
plt.plot(monthly_sales['month'], monthly_sales['total_sales'], marker='o')
plt.xticks(rotation=45)
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.show()

# Top 10 products
plt.figure(figsize=(10, 5))
sns.barplot(x='total_sales', y='Product Name', data=top_products, palette='viridis')
plt.title("Top 10 Products by Sales")
plt.xlabel("Total Sales")
plt.ylabel("Product Name")
plt.tight_layout()
plt.show()

# Sales by category
plt.figure(figsize=(6, 6))
plt.pie(category_sales['total_sales'], labels=category_sales['Category'], autopct='%1.1f%%', startangle=140)
plt.title("Sales by Category")
plt.tight_layout()
plt.show()

conn.close()
