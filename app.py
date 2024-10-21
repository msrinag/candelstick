import datetime as dt
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# Step 1: Configure Streamlit App
st.set_page_config(page_title="Stock Candlestick Plot", layout="wide")
st.title("Stock Candlestick Chart with Moving Averages and Volume")

# Step 2: Get stock market data using Yahoo Finance via yfinance
start_date = dt.datetime(2020, 1, 1)
end_date = dt.datetime.now()

# Let the user select a stock symbol
stock_symbol = st.text_input("Enter Stock Symbol", "AAPL")

# Fetch data from Yahoo Finance
df = yf.download(stock_symbol, start=start_date, end=end_date)

# Step 3: Construct moving average terms using pandas' rolling function
df['MA50'] = df['Close'].rolling(window=50, min_periods=0).mean()
df['MA200'] = df['Close'].rolling(window=200, min_periods=0).mean()

# Step 4: Create the figure and add the candlestick chart with moving averages and volume subplot
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    subplot_titles=(f"{stock_symbol} Price", "Volume"),
                    row_width=[0.2, 0.7])

# Add candlestick chart
fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'],
                             name='Candlestick'),
              row=1, col=1)

# Add 50-day moving average
fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA50'],
                         mode='lines',
                         name='50-Day MA',
                         line=dict(color='gray')),
              row=1, col=1)

# Add 200-day moving average
fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA200'],
                         mode='lines',
                         name='200-Day MA',
                         line=dict(color='lightgray')),
              row=1, col=1)

# Add volume bar chart
fig.add_trace(go.Bar(x=df.index,
                     y=df['Volume'],
                     name='Volume',
                     marker_color='red'),
              row=2, col=1)

# Step 5: Update layout - Title, Background, and Axis Labels
fig.update_layout(
    title=f'{stock_symbol} Historical Price Chart',
    xaxis_title='Date',
    yaxis_title='Price (USD $/share)',
    plot_bgcolor='lightsteelblue',
    showlegend=True,
    xaxis_rangeslider_visible=False,  # Remove the default range slider
    height=600,
    width=1000,
    margin=dict(l=50, r=50, b=100, t=100, pad=4),
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)
