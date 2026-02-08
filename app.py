import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="☕ Coffee Shop Sales Dashboard",
    layout="wide"
)

st.title("☕ Coffee Shop Sales – Interactive Dashboard")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("CoffeeShopSales-cleaned.csv")
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['month'] = df['transaction_date'].dt.month_name()
    return df

df = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Filters")

location = st.sidebar.selectbox(
    "Select Store Location",
    ["All"] + sorted(df["store_location"].unique().tolist())
)

category = st.sidebar.selectbox(
    "Select Product Category",
    ["All"] + sorted(df["product_category"].unique().tolist())
)

month = st.sidebar.selectbox(
    "Select Month",
    ["All"] + sorted(df["month"].unique().tolist())
)

# ---------------- APPLY FILTERS ----------------
filtered_df = df.copy()

if location != "All":
    filtered_df = filtered_df[filtered_df["store_location"] == location]

if category != "All":
    filtered_df = filtered_df[filtered_df["product_category"] == category]

if month != "All":
    filtered_df = filtered_df[filtered_df["month"] == month]

# ---------------- KPI METRICS ----------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Revenue",
    f"₹ {filtered_df['total_amount'].sum():,.0f}"
)

col2.metric(
    "Total Transactions",
    filtered_df.shape[0]
)

col3.metric(
    "Total Quantity Sold",
    int(filtered_df["transaction_qty"].sum())
)

# ---------------- SALES BY PRODUCT TYPE ----------------
st.subheader("📦 Sales by Product Type")

sales_by_product = (
    filtered_df
    .groupby("product_type")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

st.dataframe(sales_by_product)

# ---------------- WEEKDAY ANALYSIS ----------------
st.subheader("📅 Average Sales by Weekday")

weekday_sales = (
    filtered_df
    .groupby("weekday")["total_amount"]
    .mean()
    .sort_values()
)

st.dataframe(weekday_sales)

# ---------------- PIVOT TABLE ----------------
st.subheader("📊 Category vs Store Location")

pivot = pd.pivot_table(
    filtered_df,
    index="product_category",
    columns="store_location",
    values="total_amount",
    aggfunc="sum",
    fill_value=0
)

st.dataframe(pivot)

# ---------------- RAW DATA ----------------
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df)
