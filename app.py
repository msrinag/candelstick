import datetime as dt
import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.express as px

# Step 1: Set up the Streamlit app
st.title("Stock Price Visualization")

# Define date range for data selection
start_date = st.date_input("Start Date", value=dt.datetime(2020, 1, 1))
end_date = st.date_input("End Date", value=dt.datetime.now())

# Input for stock symbol
stock_symbol = st.text_input("Stock Symbol", value='AAPL').upper()

# Step 2: Get stock market data using Yahoo Finance
if stock_symbol:
    df = yf.download(stock_symbol, start=start_date, end=end_date)

    # Display the dataframe for debugging
    st.write("DataFrame preview:", df.head())

    # Ensure data is not empty and contains required columns
    if not df.empty and 'Close' in df.columns and 'Volume' in df.columns:
        # Drop rows with NaN in 'Close' or 'Volume' columns
        df = df.dropna(subset=['Close', 'Volume'])

        # Step 3: Construct moving average terms using pandas' rolling function
        df['MA50'] = df['Close'].rolling(window=50).mean()
        df['MA200'] = df['Close'].rolling(window=200).mean()

        # Step 4: Create a line plot for the closing price and moving averages
        fig = px.line(df, x=df.index, y='Close', title=f'{stock_symbol} Historical Price Chart', 
                      labels={'Close': 'Price (USD $/share)'})
        
        # Add moving averages
        fig.add_scatter(x=df.index, y=df['MA50'], mode='lines', name='50-Day MA', line=dict(color='gray'))
        fig.add_scatter(x=df.index, y=df['MA200'], mode='lines', name='200-Day MA', line=dict(color='lightgray'))

        # Step 5: Create a bar plot for the volume
        volume_fig = px.bar(df, x=df.index, y='Volume', title='Volume', 
                            labels={'Volume': 'Volume'}, 
                            color_discrete_sequence=['red'])

        # Update layo
