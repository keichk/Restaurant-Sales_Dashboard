import pandas as pd
import numpy as np
import streamlit as st
import datetime
import plotly.express as px

st.set_page_config(page_title="📈 Sales Dashboard", layout="wide")
PASSWORD = "dashboard123"
#st.sidebar.title("🔒 Login")
#password = st.sidebar.text_input("Enter password:", type="password")
#if password != PASSWORD:
#    st.warning("Enter the correct password to access the dashboard.")
#    st.stop()
st.sidebar.success("Welcome to the Sales Dashboard! Please upload your sales data.")

def load_data():
    expected_columns = {'date', 'item_name', 'item_type', 'item_price', 'transaction_amount', 'transaction_type', 'received_by', 'quantity'}
    # Load the dataset
    uploaded_file = st.file_uploader("Upload your sales CSV or Excel file", type=None)
    if uploaded_file is not None:
        try:  
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, index_col=0)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file, index_col=0)
            else:
                st.warning("Unsupported file format. Please upload a CSV or Excel file.")
                return None
            actual_columns = set(df.columns)
            if not expected_columns.issubset(actual_columns):
                st.warning("The uploaded file does not contain the required columns.")
                return None

            return df
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None

    else:
        st.info("No file uploaded. Loading demo file...")
        demo_file = "Balaji Fast Food Sales.csv"
        df = pd.read_csv(demo_file, index_col=0)
        return df
    

def clean_data(df):
    # Clean the dataset
    if 'date' not in df.columns:
        raise ValueError("Incompatible data format.")
    df['date'] = df['date'].str.replace('-', '/')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.sort_values(by='date', ascending=True)

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
    filtered_data = df.loc[mask].reset_index(drop=True)
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

def forecast_next_month_sales(df):
    daily_sales = df.groupby('date')['total'].sum()
    avg_daily = daily_sales.mean()
    next_month = (df['date'].max() + pd.DateOffset(months=1)).month
    forecast = avg_daily * 30  # approximation
    return forecast

data = load_data()
if data is not None:
    try:
        data = clean_data(data)
    except ValueError as e:
        st.error(f"Error cleaning data: {e}")
        st.stop()
    st.title("📊 Restaurant Sales Dashboard")
    st.sidebar.title("Filters")
    date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(data['date'].min(), data['date'].max()),
    min_value=data['date'].min(),
    max_value=data['date'].max()
    )

    # Split start and end dates
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_data = filter_data(data, start_date, end_date)
    else:
        st.warning("Please select a valid date range.")
        filtered_data = data

    # Display filtered data
    if filtered_data.empty:
        st.write("🔴 No data available for the selected period.")
    else:
        st.write("Data available for the selected period.")

    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Total Sales ", f"€{calculate_sales(filtered_data):,.2f}")
    with col2:
        st.metric("📈 Estimated Profit", f"€{calculate_profit(filtered_data):,.2f}")
    with col3:
        st.metric("📅 Forecast Next Month", f"€{forecast_next_month_sales(filtered_data):,.2f}")

    st.subheader("📦 Sales Data Table")
    st.dataframe(filtered_data.reset_index(drop=True), use_container_width=True)

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
    st.markdown("[🔗 (WhatsApp: +33 7 65 24 22 31)](https://wa.me/33765242231)")