import datetime as dt
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
import streamlit as st

st.title("Stock Price Analysis")

# User input for stock symbol
stock_symbol = st.text_input("Enter stock symbol (e.g., AAPL):", "AAPL")

# Date range selection
start_date = st.date_input("Start date", dt.date(2020, 1, 1))
end_date = st.date_input("End date", dt.date.today())

if st.button("Generate Chart"):
    # Download stock data
    df = yf.download(stock_symbol, start=start_date, end=end_date)

    # Calculate moving averages
    df['MA50'] = df['Close'].rolling(window=50, min_periods=0).mean()
    df['MA200'] = df['Close'].rolling(window=200, min_periods=0).mean()

    # Create the figure
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=(f"{stock_symbol} Price", "Volume"),
                        row_heights=[0.7, 0.3])

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

    # Update layout
    fig.update_layout(
        title=f'{stock_symbol} Historical Price Chart',
        xaxis_title='Date',
        yaxis_title='Price (USD $/share)',
        plot_bgcolor='lightsteelblue',
        showlegend=True,
        xaxis_rangeslider_visible=False,
        height=600,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
    )

    # Display the chart using Streamlit
    st.plotly_chart(fig, use_container_width=True)
