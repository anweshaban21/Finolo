import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

@st.cache_data(ttl=3600)
def get_stock_list():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    table = pd.read_html(url)[0]
    return dict(zip(table['Security'], table['Symbol']))



@st.cache_data(ttl=3600)
def fetch_stock_data(symbol, start_date, end_date):
    return yf.download(symbol, start=start_date, end=end_date)



# Streamlit app
st.set_page_config(page_title="Financial Advisor App", layout="wide")

st.title("Financial Advisor App")
if 'user' not in st.session_state:
    st.session_state.user = None
if st.session_state.user is None:
    auth_choice = st.sidebar.selectbox("Choose action", ["Login", "Register"])
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    goal=st.sidebar.selectbox("Set a Goal", ["Short-term", "Mid-term","Long-term"])
    if st.session_state:
    # Main app content
        stock_list = get_stock_list()
        selected_stock = st.selectbox("Select a stock", list(stock_list.keys()))
        symbol = stock_list[selected_stock]
    
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date", datetime.now() - timedelta(days=365))
        with col2:
            end_date = st.date_input("End date", datetime.now())
    
        data = fetch_stock_data(symbol, start_date, end_date)
        st.dataframe(data)