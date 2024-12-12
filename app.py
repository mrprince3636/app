import streamlit as st
import yfinance as yf
import pandas as pd
import time
import os
from datetime import datetime

# Define stock symbols and corresponding company names
stock_details = {
    'RELIANCE.NS': "Reliance Industries",
    'TCS.NS': "Tata Consultancy Services",
    'INFY.NS': "Infosys",
    'HDFCBANK.NS': "HDFC Bank",
    # Add more symbols as needed
}

# Predefined username and password (for demo purposes)
USER_CREDENTIALS = {
    "admin": "password123",  # Replace with secure credentials
    "user1": "userpass1"
}

# Function to save user-specific trade logs
def save_user_trade_log(username, symbol, entry_price, sl_price, trg_price, exit_price, profit_or_loss, status):
    user_folder = f'user_logs/{username}'
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    trade_data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Symbol": symbol,
        "Entry Price": entry_price,
        "Stop-Loss Price": sl_price,
        "Target Price": trg_price,
        "Exit Price": exit_price,
        "Profit/Loss": profit_or_loss,
        "Status": status,
    }
    trade_df = pd.DataFrame([trade_data])
    log_file = f'{user_folder}/trade_log.csv'
    if not os.path.exists(log_file):
        trade_df.to_csv(log_file, mode='w', index=False, header=True)
    else:
        trade_df.to_csv(log_file, mode='a', index=False, header=False)

# Function to fetch stock data
def fetch_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        return data[['Close']]
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return None

# Function for live trade monitoring
def live_virtual_trade(username, symbol, lot_size, sl_percent, trg_percent):
    st.write(f"### **Live Virtual Trade for {symbol}**")
    stock_data = fetch_stock_data(symbol)
    if stock_data is None:
        st.error("Error fetching live data. Exiting trade monitoring.")
        return

    entry_price = stock_data['Close'].iloc[-1]
    st.write(f"**Entry Price (Market Price):** ₹{entry_price:.2f}")
    sl_price = entry_price * (1 - sl_percent / 100)
    trg_price = entry_price * (1 + trg_percent / 100)

    st.write(f"**Stop-Loss Price:** ₹{sl_price:.2f}")
    st.write(f"**Target Price:** ₹{trg_price:.2f}")
    current_price_box = st.empty()

    st.write("### **Monitoring Trade...**")
    trade_open = True
    while trade_open:
        stock_data = fetch_stock_data(symbol)
        if stock_data is None:
            st.error("Error fetching live data. Exiting trade monitoring.")
            break
        current_price = stock_data['Close'].iloc[-1]
        current_price_box.metric(label="**Current Price**", value=f"₹{current_price:.2f}")
        if current_price <= sl_price:
            st.error("**Stop-Loss Hit!** Trade Closed.")
            loss = (entry_price - sl_price) * lot_size
            st.write(f"**Loss:** ₹{loss:.2f}")
            save_user_trade_log(username, symbol, entry_price, sl_price, trg_price, current_price, loss, "Stop-Loss Hit")
            trade_open = False
        elif current_price >= trg_price:
            st.success("**Target Hit!** Trade Closed.")
            profit = (trg_price - entry_price) * lot_size
            st.write(f"**Profit:** ₹{profit:.2f}")
            save_user_trade_log(username, symbol, entry_price, sl_price, trg_price, current_price, profit, "Target Hit")
            trade_open = False
        time.sleep(5)
    st.write("### **Trade Monitoring Ended.**")
    st.write("---")

# Main App
def main(username):
    st.sidebar.header("📝 **Trade Setup**")
    symbol = st.sidebar.selectbox("Select Stock", list(stock_details.keys()), format_func=lambda x: stock_details[x])
    lot_size = st.sidebar.number_input("Lot Size", min_value=1, value=1, step=1)
    sl_percent = st.sidebar.slider("Stop-Loss %", min_value=1, max_value=50, value=10)
    trg_percent = st.sidebar.slider("Target %", min_value=1, max_value=100, value=25)

    st.sidebar.write("---")
    st.sidebar.markdown("### **App Controls**")
    if st.sidebar.button("Start Live Trade"):
        live_virtual_trade(username, symbol, lot_size, sl_percent, trg_percent)

    st.write(f"### **Trade Logs for {username}**")
    user_log_file = f'user_logs/{username}/trade_log.csv'
    if os.path.exists(user_log_file):
        df = pd.read_csv(user_log_file)
        st.dataframe(df)
    else:
        st.write("No trades logged yet.")
    st.write("---")

# Login function
def login():
    st.title("🔒 **Login to Virtual Trading App**")
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.success("Login successful! Redirecting to the app...")
            st.session_state["username"] = username
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid username or password")

# Authentication check
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
    main(st.session_state["username"])
