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

    # Check if data is available
    if df.empty:
        st.error("No data available for the selected stock and date range.")
    else:
        # Calculate moving averages
        df['MA50'] = df['Close'].rolling(window=50).mean()
        df['MA200'] = df['Close'].rolling(window=200).mean()

        # Create the figure
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            vertical_spacing=0.1,
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
                                 line=dict(color='orange', width=1)),
                      row=1, col=1)

        # Add 200-day moving average
        fig.add_trace(go.Scatter(x=df.index,
                                 y=df['MA200'],
                                 mode='lines',
                                 name='200-Day MA',
                                 line=dict(color='green', width=1)),
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
            xaxis_rangeslider_visible=False,
            plot_bgcolor='white',
            hovermode='x unified',
            height=600,
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            margin=dict(l=50, r=50, b=50, t=50, pad=4)
        )

        # Update y-axes
        fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)

        # Display the chart using Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Display the data
        st.write(df)
