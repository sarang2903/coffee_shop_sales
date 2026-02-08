import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="☕ Coffee Shop Sales Analysis", layout="wide")

st.title("☕ Coffee Shop Sales Analysis (EDA)")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("CoffeeShopSales-cleaned.csv")
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['month'] = df['transaction_date'].dt.month_name()
    return df

df = load_data()

# Show raw data
st.subheader("📄 Raw Dataset")
st.dataframe(df)

# Unique values & counts
st.subheader("🔍 Categorical Columns Overview")

cols = ['store_location', 'product_category', 'product_type',
        'product_detail', 'weekday', 'month']

for col in cols:
    with st.expander(f"{col}"):
        st.write("**Unique values:**")
        st.write(df[col].unique())
        st.write("**Value counts:**")
        st.write(df[col].value_counts())

# Aggregations
st.subheader("📊 Sales Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("### Sales by Store Location")
    st.dataframe(df.groupby('store_location')['total_amount'].sum())

with col2:
    st.write("### Sales by Month")
    st.dataframe(df.groupby('month')['total_amount'].sum())

with col3:
    st.write("### Sales by Product Category")
    st.dataframe(df.groupby('product_category')['total_amount'].sum())

# Top categories
st.subheader("🏆 Top Performing Products")

col4, col5 = st.columns(2)

with col4:
    st.write("### Top 5 Product Categories (Revenue)")
    st.dataframe(
        df.groupby('product_category')['total_amount']
        .sum()
        .nlargest(5)
    )

with col5:
    st.write("### Top 10 Product Types (Quantity Sold)")
    st.dataframe(
        df.groupby('product_type')['transaction_qty']
        .sum()
        .nlargest(10)
    )

# Least selling products
st.subheader("📉 Least Selling Product Types")
st.dataframe(
    df.groupby('product_type')['transaction_qty']
    .sum()
    .nsmallest(10)
)

# Average weekday sales
st.subheader("📅 Average Sales by Weekday")
st.dataframe(df.groupby('weekday')['total_amount'].mean())

# Pivot tables
st.subheader("📌 Pivot Tables")

st.write("### Product Category vs Store Location")
st.dataframe(
    pd.pivot_table(
        df,
        index='product_category',
        columns='store_location',
        values='total_amount',
        aggfunc='sum',
        margins=True
    )
)

st.write("### Weekday vs Store Location")
st.dataframe(
    pd.pivot_table(
        df,
        index='weekday',
        columns='store_location',
        values='total_amount',
        aggfunc='sum',
        margins=True
    )
)

st.write("### Product Type vs Product Category")
st.dataframe(
    pd.pivot_table(
        df,
        index='product_type',
        columns='product_category',
        values='transaction_qty',
        aggfunc='sum',
        margins=True
    )
)

st.write("### Month vs Product Category")
st.dataframe(
    pd.pivot_table(
        df,
        index='month',
        columns='product_category',
        values='transaction_qty',
        aggfunc='sum',
        margins=True
    )
)

# User interaction section
st.subheader("🎯 Custom Analysis")

location = st.selectbox(
    "Select Store Location",
    df['store_location'].unique()
)

category = st.selectbox(
    "Select Product Category",
    df['product_category'].unique()
)

filtered_df = df[
    (df['store_location'] == location) &
    (df['product_category'] == category)
]

st.write(f"### Total Sales by Product Type in **{location}** ({category})")
st.dataframe(
    filtered_df.groupby('product_type')['total_amount'].sum()
)
