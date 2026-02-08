import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Coffee Shop Sales Dashboard", layout="wide")

st.title("☕ Coffee Shop Sales Dashboard")
st.markdown("Interactive insights into coffee shop sales performance.")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("CoffeeShopSales-cleaned.csv")
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['month'] = df['transaction_date'].dt.month_name()
    return df

df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("🔎 Filter Data")

location = st.sidebar.selectbox(
    "Store Location",
    ["All"] + sorted(df['store_location'].unique())
)

category = st.sidebar.selectbox(
    "Product Category",
    ["All"] + sorted(df['product_category'].unique())
)

month = st.sidebar.selectbox(
    "Month",
    ["All"] + sorted(df['month'].unique())
)

# --------------------------------------------------
# Apply Filters
# --------------------------------------------------
filtered_df = df.copy()

if location != "All":
    filtered_df = filtered_df[filtered_df['store_location'] == location]

if category != "All":
    filtered_df = filtered_df[filtered_df['product_category'] == category]

if month != "All":
    filtered_df = filtered_df[filtered_df['month'] == month]

# --------------------------------------------------
# KPI Section
# --------------------------------------------------
st.subheader("📊 Key Performance Indicators")

k1, k2, k3 = st.columns(3)

k1.metric("💰 Total Sales", f"{filtered_df['total_amount'].sum():,.0f}")
k2.metric("🧾 Transactions", filtered_df.shape[0])
k3.metric("☕ Quantity Sold", filtered_df['transaction_qty'].sum())

# --------------------------------------------------
# Sales by Location (Bar Chart)
# --------------------------------------------------
st.divider()
st.subheader("📍 Sales by Store Location")

sales_location = filtered_df.groupby('store_location')['total_amount'].sum()

fig, ax = plt.subplots()
sales_location.plot(kind='bar', ax=ax)
ax.set_ylabel("Total Sales")
ax.set_xlabel("Store Location")
st.pyplot(fig)

# --------------------------------------------------
# Monthly Sales Trend (Line Chart)
# --------------------------------------------------
st.divider()
st.subheader("📈 Monthly Sales Trend")

monthly_sales = filtered_df.groupby('month')['total_amount'].sum()

fig, ax = plt.subplots()
monthly_sales.plot(kind='line', marker='o', ax=ax)
ax.set_ylabel("Total Sales")
ax.set_xlabel("Month")
st.pyplot(fig)

# --------------------------------------------------
# Top Products
# --------------------------------------------------
st.divider()
st.subheader("🛍 Top Performing Products")

col1, col2 = st.columns(2)

with col1:
    st.write("### Top 10 Products by Quantity")
    st.dataframe(
        filtered_df.groupby('product_type')['transaction_qty']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

with col2:
    st.write("### Top 5 Categories by Sales")
    st.dataframe(
        filtered_df.groupby('product_category')['total_amount']
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

# --------------------------------------------------
# Weekday Analysis (Bar Chart)
# --------------------------------------------------
st.divider()
st.subheader("📅 Average Sales by Weekday")

weekday_avg = filtered_df.groupby('weekday')['total_amount'].mean()

fig, ax = plt.subplots()
weekday_avg.plot(kind='bar', ax=ax)
ax.set_ylabel("Average Sales")
ax.set_xlabel("Weekday")
st.pyplot(fig)

# --------------------------------------------------
# Pivot Table Explorer
# --------------------------------------------------
st.divider()
st.subheader("📐 Pivot Table Explorer")

pivot_choice = st.selectbox(
    "Select View",
    [
        "Category vs Location (Sales)",
        "Weekday vs Location (Sales)",
        "Month vs Category (Quantity)"
    ]
)

if pivot_choice == "Category vs Location (Sales)":
    pivot = pd.pivot_table(
        filtered_df,
        index='product_category',
        columns='store_location',
        values='total_amount',
        aggfunc='sum'
    )

elif pivot_choice == "Weekday vs Location (Sales)":
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

# --------------------------------------------------
# Product Drill Down
# --------------------------------------------------
st.divider()
st.subheader("🔍 Product Drill Down")

product = st.selectbox(
    "Select Product Type",
    sorted(filtered_df['product_type'].unique())
)

product_df = filtered_df[filtered_df['product_type'] == product]

fig, ax = plt.subplots()
product_df.groupby('store_location')['total_amount'].sum().plot(
    kind='bar', ax=ax
)
ax.set_ylabel("Total Sales")
ax.set_xlabel("Store Location")
st.pyplot(fig)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption("Coffee Shop Sales Dashboard | Streamlit Project")
