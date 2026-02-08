import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Coffee Shop Sales Dashboard", layout="wide")

st.title("☕ Coffee Shop Sales Dashboard")
st.markdown("Interactive sales insights across locations, products, and time.")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("CoffeeShopSales-cleaned.csv")
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['month'] = df['transaction_date'].dt.month_name()
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")

location = st.sidebar.selectbox(
    "Select Store Location",
    ["All"] + list(df['store_location'].unique())
)

category = st.sidebar.selectbox(
    "Select Product Category",
    ["All"] + list(df['product_category'].unique())
)

month = st.sidebar.selectbox(
    "Select Month",
    ["All"] + list(df['month'].unique())
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df.copy()

if location != "All":
    filtered_df = filtered_df[filtered_df['store_location'] == location]

if category != "All":
    filtered_df = filtered_df[filtered_df['product_category'] == category]

if month != "All":
    filtered_df = filtered_df[filtered_df['month'] == month]

# -----------------------------
# KPIs
# -----------------------------
st.subheader("📊 Key Metrics")

c1, c2, c3 = st.columns(3)

c1.metric("💰 Total Sales", f"{filtered_df['total_amount'].sum():,.0f}")
c2.metric("🧾 Transactions", filtered_df.shape[0])
c3.metric("☕ Quantity Sold", filtered_df['transaction_qty'].sum())

# -----------------------------
# Sales Analysis
# -----------------------------
st.divider()
st.subheader("📍 Sales Analysis")

col1, col2 = st.columns(2)

with col1:
    st.write("### Sales by Store Location")
    sales_loc = filtered_df.groupby('store_location')['total_amount'].sum()
    st.dataframe(sales_loc)

    fig, ax = plt.subplots(figsize=(4, 3))   # SMALL GRAPH
    sales_loc.plot(kind='bar', ax=ax)
    ax.set_ylabel("Sales")
    st.pyplot(fig)

with col2:
    st.write("### Sales by Month")
    sales_month = filtered_df.groupby('month')['total_amount'].sum()
    st.dataframe(sales_month)

    fig, ax = plt.subplots(figsize=(4, 3))   # SMALL GRAPH
    sales_month.plot(kind='line', marker='o', ax=ax)
    ax.set_ylabel("Sales")
    st.pyplot(fig)

# -----------------------------
# Product Insights
# -----------------------------
st.divider()
st.subheader("🛍 Product Insights")

col1, col2 = st.columns(2)

with col1:
    st.write("### Top 10 Products by Quantity")
    top_products = (
        filtered_df.groupby('product_type')['transaction_qty']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.dataframe(top_products)

    fig, ax = plt.subplots(figsize=(4, 3))
    top_products.plot(kind='bar', ax=ax)
    ax.set_ylabel("Quantity")
    st.pyplot(fig)

with col2:
    st.write("### Top 5 Product Categories by Sales")
    top_categories = (
        filtered_df.groupby('product_category')['total_amount']
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    st.dataframe(top_categories)

    fig, ax = plt.subplots(figsize=(4, 3))
    top_categories.plot(kind='bar', ax=ax)
    ax.set_ylabel("Sales")
    st.pyplot(fig)

# -----------------------------
# Weekday Performance
# -----------------------------
st.divider()
st.subheader("📅 Weekday Performance")

weekday_avg = (
    filtered_df.groupby('weekday')['total_amount']
    .mean()
    .sort_values(ascending=False)
)

st.dataframe(weekday_avg)

fig, ax = plt.subplots(figsize=(4, 3))
weekday_avg.plot(kind='bar', ax=ax)
ax.set_ylabel("Average Sales")
st.pyplot(fig)

# -----------------------------
# Pivot Table Section
# -----------------------------
st.divider()
st.subheader("📐 Pivot Table Explorer")

pivot_option = st.selectbox(
    "Choose Pivot View",
    [
        "Product Category vs Store Location",
        "Weekday vs Store Location",
        "Month vs Product Category"
    ]
)

if pivot_option == "Product Category vs Store Location":
    pivot = pd.pivot_table(
        filtered_df,
        index='product_category',
        columns='store_location',
        values='total_amount',
        aggfunc='sum'
    )

elif pivot_option == "Weekday vs Store Location":
    pivot = pd.pivot_table(
        filtered_df,
        index='weekday',
        columns='store_location',
        values='total_amount',
        aggfunc='sum'
    )

else:
    pivot = pd.pivot_table(
        filtered_df,
        index='month',
        columns='product_category',
        values='transaction_qty',
        aggfunc='sum'
    )

st.dataframe(pivot)

# -----------------------------
# Product Drill Down
# -----------------------------
st.divider()
st.subheader("🔍 Product Drill Down")

selected_product = st.selectbox(
    "Select Product Type",
    filtered_df['product_type'].unique()
)

product_df = filtered_df[filtered_df['product_type'] == selected_product]
product_sales = product_df.groupby('store_location')['total_amount'].sum()

st.dataframe(product_sales)

fig, ax = plt.subplots(figsize=(4, 3))
product_sales.plot(kind='bar', ax=ax)
ax.set_ylabel("Sales")
st.pyplot(fig)

# -----------------------------
# Footer
# -----------------------------
st.caption("Built with Streamlit | Coffee Shop Sales Analysis")
