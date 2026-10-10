# ApexPlanet Internship Task 3: Sales Deep-Dive Dashboard

## Project Overview
An interactive sales analytics dashboard developed using Python, Pandas, Plotly, and Streamlit as part of the ApexPlanet Data Analytics Internship.

## Objectives
- Track key sales performance indicators (KPIs).
- Analyze monthly sales trends and category-wise revenue.
- Perform customer segmentation based on spending.
- Explore data through interactive dashboard filters.

## Technology Stack
- Python
- Pandas
- Plotly
- Streamlit

## KPIs
- **Total Sales:** Sum of `Total_Sales`.
- **Unique Orders:** Count of distinct `Order_ID`.
- **Average Order Value:** Total Sales divided by Unique Orders.
- **Unique Customers:** Count of distinct `Customer_ID`.

## Customer Segmentation
Customers are divided into two groups based on total spending:
- **High Value:** Spending at or above the 75th percentile.
- **Regular:** Spending below the 75th percentile.

This is rule-based segmentation, not machine-learning clustering.

## Dashboard Features
- Date, category, gender, and city filters.
- Monthly sales trend.
- Revenue by category.
- Customer segment comparisons.
- Top customers table.
- Filtered data CSV download.

## Dataset
The dataset contains 1,000 rows. The original CSV has 992 unique orders and 947 unique customers. Total sales in the original CSV are ₹13,939,9439.65? 

**Note:** Confirm the correct Indian-number formatting of total sales before using this figure in the final report.

## Run Locally
1. Install Python 3.10 or newer.
2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

## Project Files
- `app.py`: Dashboard application.
- `dataset_converted.csv`: Sales dataset.
- `deep_drive_analysis.ipynb`: Analysis notebook.
- `requirements.txt`: Dependencies.

## Status
Local dashboard is running. Public deployment link will be added after deployment.
