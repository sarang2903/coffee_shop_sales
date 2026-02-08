import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="☕ Coffee Shop Sales Dashboard",
    layout="wide"
)

st.title("☕ Coffee Shop Sales – Interactive Analysis (No Charts)")

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
    "Store Location",
    ["All"] + sorted(df["store_location"].unique())
)

category = st.sidebar.selectbox(
    "Product Category",
    ["All"] + sorted(df["product_category"].unique())
)

month = st.sidebar.selectbox(
    "Month",
    ["All"] + sorted(df["month"].unique())
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
st.subheader("📦 Revenue by Product Type")

product_sales = (
    filtered_df
    .groupby("product_type", as_index=False)["total_amount"]
    .sum()
    .sort_values(by="total_amount", ascending=False)
)

st.dataframe(product_sales)

# ---------------- WEEKDAY PERFORMANCE ----------------
st.subheader("📅 Average Sales by Weekday")

weekday_sales = (
    filtered_df
    .groupby("weekday", as_index=False)["total_amount"]
    .mean()
    .sort_values(by="total_amount", ascending=False)
)

st.dataframe(weekday_sales)

# ---------------- TOP & BOTTOM PRODUCTS ----------------
st.subheader("🏆 Product Performance")

col4, col5 = st.columns(2)

with col4:
    st.write("### 🔝 Top 10 Products by Quantity Sold")
    top_products = (
        filtered_df
        .groupby("product_type", as_index=False)["transaction_qty"]
        .sum()
        .sort_values(by="transaction_qty", ascending=False)
        .head(10)
    )
    st.dataframe(top_products)

with col5:
    st.write("### 🔻 Bottom 10 Products by Quantity Sold")
    bottom_products = (
        filtered_df
        .groupby("product_type", as_index=False)["transaction_qty"]
        .sum()
        .sort_values(by="transaction_qty")
        .head(10)
    )
    st.dataframe(bottom_products)

# ---------------- PIVOT TABLE ----------------
st.subheader("📊 Category vs Store Location (Revenue)")

pivot_table = pd.pivot_table(
    filtered_df,
    index="product_category",
    columns="store_location",
    values="total_amount",
    aggfunc="sum",
    fill_value=0,
    margins=True
)

st.dataframe(pivot_table)

# ---------------- RAW DATA ----------------
with st.expander("📄 View Filtered Raw Data"):
    st.dataframe(filtered_df)
    
