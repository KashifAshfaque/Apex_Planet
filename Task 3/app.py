from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Deep-Dive Dashboard", page_icon="📊", layout="wide")
DATA_PATH = Path(__file__).parent / "dataset_converted.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    for col in ["Age", "Quantity", "Unit_Price", "Total_Sales"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

st.title("📊 Sales Performance: Deep-Dive & Customer Segmentation")
st.caption("APEX Planet Data Analytics Internship · Task 3 · Python + Streamlit + Plotly")

if not DATA_PATH.exists():
    st.error("Dataset not found. Put dataset_converted.csv in the same folder as app.py.")
    st.stop()

df = load_data(DATA_PATH)

with st.sidebar:
    st.header("Dashboard Filters")
    date_min, date_max = df["Order_Date"].min().date(), df["Order_Date"].max().date()
    date_range = st.date_input("Order date range", value=(date_min, date_max), min_value=date_min, max_value=date_max)
    categories = sorted(df["Category"].dropna().unique().tolist())
    selected_categories = st.multiselect("Category", categories, default=categories)
    genders = sorted(df["Gender"].dropna().unique().tolist())
    selected_genders = st.multiselect("Gender", genders, default=genders)
    cities = sorted(df["City"].dropna().unique().tolist())
    selected_cities = st.multiselect("City", cities, default=cities)

filtered = df.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[filtered["Order_Date"].dt.date.between(date_range[0], date_range[1])]
filtered = filtered[filtered["Category"].isin(selected_categories)]
filtered = filtered[filtered["Gender"].isin(selected_genders)]
filtered = filtered[filtered["City"].isin(selected_cities)]

if filtered.empty:
    st.warning("No records match these filters. Adjust the sidebar selections.")
    st.stop()

sales = filtered["Total_Sales"].sum()
orders = filtered["Order_ID"].nunique()
customers = filtered["Customer_ID"].nunique()
aov = sales / orders if orders else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Sales", f"₹{sales:,.0f}")
k2.metric("Unique Orders", f"{orders:,}")
k3.metric("Average Order Value", f"₹{aov:,.0f}")
k4.metric("Unique Customers", f"{customers:,}")

st.subheader("Sales Trends & Mix")
left, right = st.columns(2)
with left:
    monthly = filtered.dropna(subset=["Order_Date"]).assign(Month=lambda x: x["Order_Date"].dt.to_period("M").dt.to_timestamp()).groupby("Month", as_index=False)["Total_Sales"].sum()
    fig = px.line(monthly, x="Month", y="Total_Sales", markers=True, title="Monthly Sales Trend", labels={"Total_Sales":"Sales (₹)", "Month":"Month"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    cat = filtered.groupby("Category", as_index=False)["Total_Sales"].sum().sort_values("Total_Sales", ascending=False)
    fig = px.bar(cat, x="Category", y="Total_Sales", color="Category", title="Sales by Category", labels={"Total_Sales":"Sales (₹)"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer Segmentation")
customer = filtered.groupby("Customer_ID", as_index=False).agg(
    Customer_Name=("Customer_Name", "first"),
    Total_Spend=("Total_Sales", "sum"),
    Order_Count=("Order_ID", "nunique"),
    Last_Order=("Order_Date", "max"),
    Age=("Age", "median"),
    Gender=("Gender", "first"),
    City=("City", "first"),
)
spend_cut = customer["Total_Spend"].quantile(0.75) if len(customer) > 1 else customer["Total_Spend"].max()
customer["Segment"] = customer["Total_Spend"].apply(lambda x: "High Value" if x >= spend_cut else "Regular")
seg = customer.groupby("Segment", as_index=False).agg(Customers=("Customer_ID", "nunique"), Revenue=("Total_Spend", "sum"), Avg_Spend=("Total_Spend", "mean"))
sc1, sc2 = st.columns(2)
with sc1:
    fig = px.bar(seg, x="Segment", y="Customers", color="Segment", title="Customers by Spend Segment", labels={"Customers":"Unique customers"})
    st.plotly_chart(fig, use_container_width=True)
with sc2:
    fig = px.bar(seg, x="Segment", y="Revenue", color="Segment", title="Revenue by Spend Segment", labels={"Revenue":"Sales (₹)"})
    st.plotly_chart(fig, use_container_width=True)

st.caption(f"Segmentation rule: High Value = customer spend at or above the filtered dataset's 75th percentile (₹{spend_cut:,.0f}); Regular = below that threshold. This is a simple business-rule segmentation, not an ML clustering model.")

st.subheader("Top Customers")
st.dataframe(customer.sort_values("Total_Spend", ascending=False).head(10).reset_index(drop=True), use_container_width=True, hide_index=True)

with st.expander("Data quality notes"):
    st.write(f"Rows in source dataset: **{len(df):,}**")
    st.write(f"Exact duplicate rows: **{int(df.duplicated().sum()):,}**")
    st.write(f"Missing Age values: **{int(df['Age'].isna().sum()):,}**")
    st.write(f"Missing City values: **{int(df['City'].isna().sum()):,}**")
    st.write("KPIs and charts use the filtered rows. Missing Age/City values are not imputed because they are not required for the sales KPIs.")

st.download_button("Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"), file_name="filtered_sales_data.csv", mime="text/csv")
