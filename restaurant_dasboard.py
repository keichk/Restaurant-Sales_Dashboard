import pandas as pd
import numpy as np
import streamlit as st
import datetime
import plotly.express as px

st.set_page_config(page_title="📈 Sales Dashboard", layout="wide")

def load_data():
    # Load the dataset
    uploaded_file = st.file_uploader("Upload your sales CSV or Excel file", type=None)
    if uploaded_file is not None:
        if uploaded_file.name.endwith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endwith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            st.warning("Unsupported file format. Please upload a CSV or Excel file.")
            return None
        return df
    else:
        st.info("No file uploaded. Loading demo file...")
        demo_file = "Balaji Fast Food Sales.csv"
        df = pd.read_csv(demo_file)
        return df

def clean_data(df):
    # Clean the dataset
    df['date'] = df['date'].str.replace('-', '/')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Rename columns
    df.rename(columns={
        'item_name': 'name',
        'item_type': 'type',
        'item_price': 'price',
        'transaction_amount': 'total',
        'transaction_type': 'payment_mode',
        'received_by': 'clients',
    }, inplace=True)
    # Remove invalid rows
    df["payment_mode"] = df["payment_mode"].fillna(df["payment_mode"].mode()[0])

    return df

def filter_data(df, start_date, end_date):
    # Filter the dataset based on date range
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    filtered_data = df.loc[mask]
    return filtered_data

def calculate_sales(df):
    # Calculate total sales
    total_sales = df['total'].sum()
    return total_sales

def calculate_profit(df):
    # Calculate total profit
    total_sales = calculate_sales(df)
    estimated_profit = total_sales * 0.3  # Assuming 30% profit margin
    return estimated_profit

data = load_data()
if data is not None:
    data = clean_data(data) 
    st.title("📊 Restaurant Sales Dashboard")
    st.sidebar.title("Filters")
    start_date = st.sidebar.date_input("Start Date", data['date'].min())   
    end_date = st.sidebar.date_input("End Date", data['date'].max())
    filtered_data = filter_data(data, start_date, end_date)

    # Display filtered data
    if filtered_data.empty:
        st.write("🔴 No data available for the selected period.")
    else:
        st.write("Data available for the selected period.")

    # Display metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💰 Total Sales ", f"€{calculate_sales(filtered_data):,.2f}")
    with col2:
        st.metric("📈 Estimated Profit", f"€{calculate_profit(filtered_data):,.2f}")

    st.subheader("📦 Sales Data Table")
    st.dataframe(filtered_data, use_container_width=True)

    # Charts
    st.subheader("📊 Sales Over Time")
    daily_sales = filtered_data.groupby('date')['total'].sum().reset_index()
    fig1 = px.line(daily_sales, x='date', y='total', title='Total Sales per Day')
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("💳 Sales by Payment Mode")
    payment_sales = filtered_data.groupby('payment_mode')['total'].sum().reset_index()
    fig2 = px.pie(payment_sales, values='total', names='payment_mode', title='Sales by Payment Method')
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🍽️ Top Selling Items")
    top_items = filtered_data.groupby('name')['quantity'].sum().reset_index()
    top_items = top_items.sort_values(by='quantity', ascending=False).head(10)
    fig3 = px.bar(top_items, x='name', y='quantity', title='Top Selling Items')
    st.plotly_chart(fig3, use_container_width=True)

    # Export
    st.download_button("📥 Download Filtered Data", data=filtered_data.to_csv(index=False), file_name="filtered_sales.csv")


# Quick contact
st.markdown("---")
st.subheader("📦 Order now !")
st.success("Discover our best-sellers and get them delivered in just one click.")
if st.button("Order now"):
    st.write("🔗 (WhatsApp: +33 7 65 24 22 31)")
