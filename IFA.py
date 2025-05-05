import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt
import plotly.graph_objects as go

# Set the date range
start_date = dt.datetime(2025, 4, 1)
end_date = dt.datetime(2025, 5, 1)

# Define stock categories
stocks = {
    'Network': ['BHARTIARTL.NS', 'IDEA.NS', 'JIOFIN.NS'],
    'IT Sector': ['TCS.NS', 'INFY.NS', 'WIPRO.NS'],
    'Health Care': ['SUNPHARMA.NS', 'DRREDDY.NS', 'CIPLA.NS', 'LUPIN.NS', 'AUROPHARMA.NS'],
    'Real Estate': ['DLF.NS', 'GODREJPROP.NS', 'OBEROIRLTY.NS', 'PHOENIXLTD.NS', 'PRESTIGE.NS'],
    'Industrials': ['LT.NS', 'BHEL.NS', 'SIEMENS.NS', 'ABB.NS', 'HAVELLS.NS']
}

@st.cache_data(show_spinner=False)
def load_data():
    all_data = []
    for category, symbols in stocks.items():
        for symbol in symbols:
            try:
                data = yf.download(symbol, start=start_date, end=end_date)
                data['Symbol'] = symbol.split('.')[0]
                data['Category'] = category
                all_data.append(data)
            except Exception as e:
                st.error(f"Failed to fetch data for {symbol}: {e}")
    df = pd.concat(all_data).reset_index()
    return df

# Streamlit interface
st.title("📈 Stock Price Comparison Dashboard")

# Load data
df = load_data()

# Select category
category = st.selectbox("Select Category", list(stocks.keys()))
category_df = df[df['Category'] == category]

# Select two symbols
symbols = category_df['Symbol'].unique()
symbol1 = st.selectbox("Select Fi
