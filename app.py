import streamlit as st
import datetime as dt
import pandas as pd
import plotly.express as px
import yfinance as yf

import plotly
print(plotly.__version__)

st.set_page_config(layout="wide")

st.title("Stock Price Analysis")

# User input for stock symbol and date range
stock_symbol = st.text_input("Enter stock symbol (e.g., AAPL):", "AAPL")
start_date = st.date_input("Start date", dt.date(2020, 1, 1))
end_date = st.date_input("End date", dt.date.today())

# Download stock data
@st.cache_data
def load_data(symbol, start, end):
    return yf.download(symbol, start=start, end=end)

df = load_data(stock_symbol, start_date, end_date)

# Calculate moving averages
df['MA50'] = df['Close'].rolling(window=50, min_periods=0).mean()
df['MA200'] = df['Close'].rolling(window=200, min_periods=0).mean()

# Create candlestick chart
fig_candlestick = px.candlestick(df, x=df.index, open='Open', high='High', low='Low', close='Close',
                                 title=f"{stock_symbol} Price")
fig_candlestick.add_scatter(x=df.index, y=df['MA50'], mode='lines', name='50-Day MA', line=dict(color='gray'))
fig_candlestick.add_scatter(x=df.index, y=df['MA200'], mode='lines', name='200-Day MA', line=dict(color='lightgray'))

# Create volume chart
fig_volume = px.bar(df, x=df.index, y='Volume', title="Volume")

# Update layout
fig_candlestick.update_layout(xaxis_title='Date', yaxis_title='Price (USD $/share)',
                              plot_bgcolor='lightsteelblue', showlegend=True)
fig_volume.update_layout(xaxis_title='Date', yaxis_title='Volume',
                         plot_bgcolor='lightsteelblue', showlegend=False)

# Display charts
st.plotly_chart(fig_candlestick, use_container_width=True)
st.plotly_chart(fig_volume, use_container_width=True)

# Display dataframe
st.subheader("Stock Data")
st.dataframe(df)
