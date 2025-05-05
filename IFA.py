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

# App Title
st.title("📈 Stock Price Comparison Dashboard")

# Load data
df = load_data()

# Select category
category = st.selectbox("Select Category", list(stocks.keys()))
category_df = df[df['Category'] == category]

# Select two symbols
symbols = category_df['Symbol'].unique()
symbol1 = st.selectbox("Select First Symbol", symbols)
symbol2 = st.selectbox("Select Second Symbol", [s for s in symbols if s != symbol1])

# Filter data for selected stocks
stk1 = category_df[category_df['Symbol'] == symbol1]
stk2 = category_df[category_df['Symbol'] == symbol2]

# Plot using Plotly
st.subheader(f"{symbol1} vs {symbol2} - Closing Price Comparison")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=stk1['Date'],
    y=stk1['Close'],
    mode='lines+markers',
    name=symbol1
))

fig.add_trace(go.Scatter(
    x=stk2['Date'],
    y=stk2['Close'],
    mode='lines+markers',
    name=symbol2
))

fig.update_layout(
    title=f"{symbol1} vs {symbol2} - Closing Price",
    xaxis_title="Date",
    yaxis_title="Closing Price (INR)",
    legend_title="Stocks",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Option to download data
st.download_button(
    label="📥 Download Full Dataset as CSV",
    data=df.to_csv(index=False),
    file_name='stock_data_combined.csv',
    mime='text/csv'
)
