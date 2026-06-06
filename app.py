import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales & Revenue Analysis Dashboard")
st.write("Interactive dashboard for tracking sales, revenue, products, regions, and payment methods.")

DATASET_FILE = "Online Sales Data.csv"

if not os.path.exists(DATASET_FILE):
    st.error(f"File not found: {DATASET_FILE}")
    st.stop()

df = pd.read_csv(DATASET_FILE)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])

st.sidebar.header("Dashboard Controls")

categories = sorted(df["Product Category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Select Product Category",
    categories,
    default=categories
)

regions = sorted(df["Region"].dropna().unique())
selected_regions = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=regions
)

payments = sorted(df["Payment Method"].dropna().unique())
selected_payments = st.sidebar.multiselect(
    "Select Payment Method",
    payments,
    default=payments
)

filtered_df = df[
    (df["Product Category"].isin(selected_categories)) &
    (df["Region"].isin(selected_regions)) &
    (df["Payment Method"].isin(selected_payments))
]

if filtered_df.empty:
    st.warning("No data found for selected filters.")
    st.stop()

total_revenue = filtered_df["Total Revenue"].sum()
total_units = filtered_df["Units Sold"].sum()
total_transactions = filtered_df["Transaction ID"].nunique()
avg_revenue = filtered_df["Total Revenue"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Units Sold", f"{total_units:,}")
col3.metric("Transactions", total_transactions)
col4.metric("Average Revenue", f"${avg_revenue:,.2f}")

st.markdown("---")

chart1, chart2 = st.columns(2)

with chart1:
    st.subheader("📈 Monthly Revenue Trend")
    monthly_revenue = (
        filtered_df.groupby(filtered_df["Date"].dt.to_period("M"))["Total Revenue"]
        .sum()
    )
    monthly_revenue.index = monthly_revenue.index.astype(str)

    fig, ax = plt.subplots(figsize=(8, 5))
    monthly_revenue.plot(kind="line", marker="o", ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Revenue")
    ax.set_title("Monthly Revenue Trend")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with chart2:
    st.subheader("📊 Revenue by Product Category")
    category_revenue = (
        filtered_df.groupby("Product Category")["Total Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    category_revenue.plot(kind="bar", ax=ax)
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Total Revenue")
    ax.set_title("Revenue by Category")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

chart3, chart4 = st.columns(2)

with chart3:
    st.subheader("🏆 Top 10 Products")
    top_products = (
        filtered_df.groupby("Product Name")["Total Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    top_products.plot(kind="barh", ax=ax)
    ax.set_xlabel("Total Revenue")
    ax.set_ylabel("Product Name")
    ax.set_title("Top 10 Products by Revenue")
    st.pyplot(fig)

with chart4:
    st.subheader("🌍 Revenue by Region")
    region_revenue = (
        filtered_df.groupby("Region")["Total Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    region_revenue.plot(kind="bar", ax=ax)
    ax.set_xlabel("Region")
    ax.set_ylabel("Total Revenue")
    ax.set_title("Revenue by Region")
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.subheader("💳 Payment Method Distribution")
payment_revenue = (
    filtered_df.groupby("Payment Method")["Total Revenue"]
    .sum()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(7, 5))
payment_revenue.plot(kind="pie", autopct="%1.1f%%", ax=ax)
ax.set_ylabel("")
ax.set_title("Revenue by Payment Method")
st.pyplot(fig)

st.subheader("📋 Sales Data")
st.dataframe(filtered_df, use_container_width=True)