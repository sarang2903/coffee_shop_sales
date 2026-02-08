import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="☕ Coffee Shop Sales Dashboard",
    layout="wide"
)

st.title("☕ Coffee Shop Sales Dashboard")
st.caption("Interactive Sales Analysis & Insights")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("CoffeeShopSales-cleaned.csv")
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["month"] = df["transaction_date"].dt.month_name()
    return df

df = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Filter Data")

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

# ---------------- FILTER DATA ----------------
filtered_df = df.copy()

if location != "All":
    filtered_df = filtered_df[filtered_df["store_location"] == location]

if category != "All":
    filtered_df = filtered_df[filtered_df["product_category"] == category]

if month != "All":
    filtered_df = filtered_df[filtered_df["month"] == month]

# ---------------- KPI METRICS ----------------
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"₹ {filtered_df['total_amount'].sum():,.0f}")
col2.metric("🧾 Total Transactions", filtered_df.shape[0])
col3.metric("📦 Quantity Sold", int(filtered_df["transaction_qty"].sum()))
col4.metric("🛒 Avg Bill Value", f"₹ {filtered_df['total_amount'].mean():.0f}")

# ---------------- MONTHLY SALES TREND ----------------
st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .groupby("month")["total_amount"]
    .sum()
)

fig, ax = plt.subplots(figsize=(6, 3))
monthly_sales.plot(marker="o", ax=ax)
ax.set_ylabel("Total Sales")
ax.set_xlabel("Month")
ax.set_title("Sales Trend Over Months")
st.pyplot(fig)

# ---------------- PRODUCT PERFORMANCE ----------------
st.subheader("📦 Product Performance")

product_sales = (
    filtered_df
    .groupby("product_type")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

st.dataframe(product_sales)

fig2, ax2 = plt.subplots(figsize=(6, 3))
product_sales.head(10).plot(kind="bar", ax=ax2)
ax2.set_ylabel("Total Sales")
ax2.set_title("Top 10 Products by Revenue")
st.pyplot(fig2)

# ---------------- WEEKDAY INSIGHTS ----------------
st.subheader("📅 Weekday Insights")

weekday_avg = (
    filtered_df
    .groupby("weekday")["total_amount"]
    .mean()
    .sort_values()
)

best_day = weekday_avg.idxmax()
worst_day = weekday_avg.idxmin()

col5, col6 = st.columns(2)
col5.success(f"🔥 Best Sales Day: **{best_day}**")
col6.warning(f"❄️ Lowest Sales Day: **{worst_day}**")

fig3, ax3 = plt.subplots(figsize=(6, 3))
weekday_avg.plot(kind="barh", ax=ax3)
ax3.set_xlabel("Average Sales")
st.pyplot(fig3)

# ---------------- CATEGORY vs LOCATION ----------------
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

# ---------------- SMART INSIGHTS ----------------
st.subheader("🧠 Smart Insights")

top_product = product_sales.idxmax()
top_category = (
    filtered_df.groupby("product_category")["total_amount"]
    .sum()
    .idxmax()
)

st.info(
    f"""
    🔹 **Top Product:** {top_product}  
    🔹 **Top Category:** {top_category}  
    🔹 **Peak Sales Day:** {best_day}
    """
)

# ---------------- RAW DATA ----------------
with st.expander("📄 View Filtered Raw Data"):
    st.dataframe(filtered_df)
