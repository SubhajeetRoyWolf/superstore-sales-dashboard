import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Title
st.title("📊 Superstore Sales & Revenue Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("C:/Users/H896994/Desktop/Projects/Superstore.csv", encoding='latin1')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month_name()
    df['Profit Margin'] = df['Profit'] / df['Sales']
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df['Year'].unique())
)

region = st.sidebar.multiselect(
    "Select Region",
    df['Region'].unique(),
    default=df['Region'].unique()
)

filtered_df = df[
    (df['Year'] == year) &
    (df['Region'].isin(region))
]

# KPI Section
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
col3.metric("Profit Margin", f"{(filtered_df['Profit'].sum()/filtered_df['Sales'].sum())*100:.2f}%")
col4.metric("Total Orders", filtered_df['Order ID'].nunique())

# Charts
st.subheader("📈 Sales Analysis")

col1, col2 = st.columns(2)

# Monthly sales
with col1:
    monthly_sales = filtered_df.groupby('Month')['Sales'].sum()
    fig, ax = plt.subplots()
    monthly_sales.plot(ax=ax)
    ax.set_title("Monthly Sales Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")
    st.pyplot(fig)

# Category profit
with col2:
    fig, ax = plt.subplots()
    sns.barplot(data=filtered_df, x='Category', y='Profit', ax=ax)
    ax.set_title("Profit by Category")
    st.pyplot(fig)

# Discount vs Profit
st.subheader("💸 Discount Impact")

fig, ax = plt.subplots()
sns.scatterplot(data=filtered_df, x='Discount', y='Profit', ax=ax)
ax.set_title("Discount vs Profit")
st.pyplot(fig)

# Insights
st.subheader("🧠 Key Insights")
st.markdown("""
Technology category generates the highest profit.
Discounts above 30% frequently result in losses.
Sales peak during Q4 due to seasonal demand.
""")

# Recommendations
st.subheader("💡 Business Recommendations")
st.markdown("""
Cap discounts at 25% to protect margins.
Focus promotions on high-margin categories.
Review pricing strategy for loss-making products.
""")