import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt

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

# Load data
st.title("📈 Stock Price Comparison Dashboard")
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

# Plotting
st.subheader(f"{symbol1} vs {symbol2} - Closing Price")

fig, axs = plt.subplots(1, 2, figsize=(14, 5))

axs[0].plot(stk1['Date'], stk1['Close'], marker='o')
axs[0].set_title(symbol1)
axs[0].tick_params(axis='x', rotation=45)

axs[1].plot(stk2['Date'], stk2['Close'], marker='o', color='orange')
axs[1].set_title(symbol2)
axs[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
st.pyplot(fig)

# Option to download data
st.download_button(
    label="📥 Download Full Dataset as CSV",
    data=df.to_csv(index=False),
    file_name='stock_data_combined.csv',
    mime='text/csv'
)
