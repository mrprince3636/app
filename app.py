import streamlit as st
import yfinance as yf
import pandas as pd

# Define stock symbols and corresponding company names
stock_details = {
    'RELIANCE.NS': "Reliance Industries",
    'TCS.NS': "Tata Consultancy Services",
    'INFY.NS': "Infosys",
    'HDFCBANK.NS': "HDFC Bank",
    'ICICIBANK.NS': "ICICI Bank",
    'ADANIGREEN.NS': "ADANI GREEN",
    'ASIANPAINT.NS': "Asian Paints",
    'AXISBANK.NS': "Axis Bank",
    'BAJAJ-AUTO.NS': "Bajaj Auto",
    'BAJFINANCE.NS': "Bajaj Finance",
    'BAJAJFINSV.NS': "Bajaj Finserv",
    'BHARTIARTL.NS': "Bharti Airtel",
    'BRITANNIA.NS': "Britannia Industries",
    'CIPLA.NS': "Cipla",
    'COALINDIA.NS': "Coal India",
    'DIVISLAB.NS': "Divi's Laboratories",
    'DRREDDY.NS': "Dr. Reddy's Laboratories",
    'EICHERMOT.NS': "Eicher Motors",
    'GRASIM.NS': "Grasim Industries",
    'HCLTECH.NS': "HCL Technologies",
    'HDFCLIFE.NS': "HDFC Life Insurance",
    'HEROMOTOCO.NS': "Hero MotoCorp",
    'HINDALCO.NS': "Hindalco Industries",
    'HINDUNILVR.NS': "Hindustan Unilever",
    'INDUSINDBK.NS': "IndusInd Bank",
    'ITC.NS': "ITC Ltd",
    'JSWSTEEL.NS': "JSW Steel",
    'KOTAKBANK.NS': "Kotak Mahindra Bank",
    'LT.NS': "Larsen & Toubro",
    'M&M.NS': "Mahindra & Mahindra",
    'MARUTI.NS': "Maruti Suzuki",
    'NESTLEIND.NS': "Nestlé India",
    'NTPC.NS': "NTPC",
    'ONGC.NS': "Oil & Natural Gas Corporation",
    'POWERGRID.NS': "Power Grid Corporation",
    'SBIN.NS': "State Bank of India",
    'SUNPHARMA.NS': "Sun Pharmaceutical",
    'TATACONSUM.NS': "Tata Consumer Products",
    'TATAMOTORS.NS': "Tata Motors",
    'TATAPOWER.NS': "Tata Power",
    'TATASTEEL.NS': "Tata Steel",
    'TECHM.NS': "Tech Mahindra",
    'ULTRACEMCO.NS': "UltraTech Cement",
    'UPL.NS': "UPL Ltd",
    'WIPRO.NS': "Wipro"
    # Add other Nifty 50 stocks here
}

# Function to fetch stock data
def fetch_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="6mo")
        return data[['Close']]
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return None

# Function to calculate EMAs
def calculate_ema(data):
    data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
    data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()
    data['EMA_100'] = data['Close'].ewm(span=100, adjust=False).mean()
    return data

# Function to check crossovers
def check_ema_crossover(data):
    recent_data = data.tail(5)
    crossover_info = []
    for i in range(1, len(recent_data)):
        if recent_data['EMA_20'].iloc[i] >= recent_data['EMA_50'].iloc[i] and recent_data['EMA_20'].iloc[i-1] <= recent_data['EMA_50'].iloc[i-1]:
            crossover_info.append("Bullish crossover: EMA 20 crossed above EMA 50")
        if recent_data['EMA_20'].iloc[i] <= recent_data['EMA_50'].iloc[i] and recent_data['EMA_20'].iloc[i-1] >= recent_data['EMA_50'].iloc[i-1]:
            crossover_info.append("Bearish crossover: EMA 20 crossed below EMA 50")
    return crossover_info

# Main function to display results in UI
def display_ema_crossovers():
    st.title("Stock EMA Crossover Analysis")
    st.subheader("Bullish and Bearish EMA Crossovers")
    crossed_stocks = []

    for symbol, name in stock_details.items():
        stock_data = fetch_stock_data(symbol)
        if stock_data is not None:
            stock_data_with_ema = calculate_ema(stock_data)
            crossover_info = check_ema_crossover(stock_data_with_ema)
            if crossover_info:
                latest_price = stock_data_with_ema['Close'].iloc[-1]
                crossed_stocks.append((symbol, name, latest_price, crossover_info))
    
    if crossed_stocks:
        for stock in crossed_stocks:
            st.write(f"**Symbol:** {stock[0]} | **Name:** {stock[1]} | **Price:** ₹{stock[2]:.2f}")
            for info in stock[3]:
                st.markdown(f"- {info}")
            st.markdown("---")
    else:
        st.write("No stocks found with EMA crossovers in the last 3 days.")

# Run the app
if __name__ == '__main__':
    display_ema_crossovers()
