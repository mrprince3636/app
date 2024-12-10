import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Define stock symbols and corresponding company names
stock_details = {
    'RELIANCE.NS': "Reliance Industries",
    'TCS.NS': "Tata Consultancy Services",
    'INFY.NS': "Infosys",
    'HDFCBANK.NS': "HDFC Bank",
    # Add more symbols as needed
}

# Function to fetch stock data (real-time for the current day)
def fetch_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")  # Fetch only the current day's data
        return data[['Close']]
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return None

# Function for live trade monitoring from the current market price
def live_virtual_trade(symbol, lot_size, sl_percent, trg_percent):
    st.write(f"**Live Virtual Trade for {symbol}**")
    
    # Fetch the current market price (latest close price)
    stock_data = fetch_stock_data(symbol)
    if stock_data is None:
        st.error("Error fetching live data. Exiting trade monitoring.")
        return

    entry_price = stock_data['Close'].iloc[-1]  # Current market price as entry
    st.write(f"**Entry Price (Market Price):** ₹{entry_price:.2f}")
    
    # Calculate SL and Target Prices
    sl_price = entry_price * (1 - sl_percent / 100)
    trg_price = entry_price * (1 + trg_percent / 100)
    
    st.write(f"**Stop-Loss Price:** ₹{sl_price:.2f}")
    st.write(f"**Target Price:** ₹{trg_price:.2f}")
    st.write("---")
    
    # Placeholder for the current price (in fixed box)
    current_price_box = st.empty()

    st.write("**Monitoring Trade...**")
    trade_open = True
    while trade_open:
        # Fetch the current price again (real-time)
        stock_data = fetch_stock_data(symbol)
        if stock_data is None:
            st.error("Error fetching live data. Exiting trade monitoring.")
            break
        current_price = stock_data['Close'].iloc[-1]

        # Update the placeholder with the current price
        current_price_box.metric(label="**Current Price**", value=f"₹{current_price:.2f}")

        # Check if Stop-Loss or Target is hit
        if current_price <= sl_price:
            st.error("**Stop-Loss Hit!** Trade Closed.")
            loss = (entry_price - sl_price) * lot_size
            st.write(f"**Loss:** ₹{loss:.2f}")
            trade_open = False
        elif current_price >= trg_price:
            st.success("**Target Hit!** Trade Closed.")
            profit = (trg_price - entry_price) * lot_size
            st.write(f"**Profit:** ₹{profit:.2f}")
            trade_open = False

        # Wait before fetching the next price
        time.sleep(5)  # Sleep 5 seconds before checking again

    st.write("**Trade Monitoring Ended.**")
    st.write("---")

# Main App
def main():
    st.title("Live Virtual Trade Simulation App")
    
    # User selects the stock and trade parameters
    symbol = st.selectbox("Select Stock", list(stock_details.keys()), format_func=lambda x: stock_details[x])
    lot_size = st.number_input("Lot Size", min_value=1, value=1)
    sl_percent = st.slider("Stop-Loss %", min_value=1, max_value=50, value=10)
    trg_percent = st.slider("Target %", min_value=1, max_value=100, value=25)

    if st.button("Start Live Trade"):
        live_virtual_trade(symbol, lot_size, sl_percent, trg_percent)

# Run the app
if __name__ == "__main__":
    main()
