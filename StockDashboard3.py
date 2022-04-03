import datetime
import requests
from PIL import Image
from pymongo import MongoClient
import hashlib
import plotly.graph_objs as go
import pandas as pd
import yfinance as yf
import streamlit as st

client = MongoClient('localhost', 27017)
db = client["stocks"]
col = db["stock_metadata"]
db2 = client["Validate"]
col2 = db2["Login"]

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; '
            'x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

main_url = "https://www.nseindia.com/"
response = requests.get(main_url, headers=headers)
print(response.status_code)
cookies = response.cookies


def live_data():
    yf.pdr_override()

    # Create input field for our desired stock
    tickers = pd.read_html('https://ournifty.com/stock-list-in-nse-fo-futures-and-options.html#:~:text=NSE%20F%26O%20Stock%'
                           '20List%3A%20%20%20%20SL,%20%201000%20%2052%20more%20rows%20')[0]

    tickers = tickers.SYMBOL.to_list()

    for count in range(len(tickers)):
        tickers[count] = tickers[count] + ".NS"

    stock_symbol = st.selectbox("Select company", tickers)

    # Retrieve stock data frame (df) from yfinance API at an interval of 1m

    if st.button(label="Click"):
        df = yf.download(tickers=stock_symbol, period='1d', interval='1m')
        fig = go.Figure()

        fig.add_trace(go.Candlestick(x=df.index,
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'], name='market data'))

        fig.update_layout(
            title=str(stock_symbol) + ' Live Share Price:',
            yaxis_title='Stock Price (USD per Shares)')

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=15, label="15m", step="minute", stepmode="backward"),
                    dict(count=45, label="45m", step="minute", stepmode="backward"),
                    dict(count=1, label="HTD", step="hour", stepmode="todate"),
                    dict(count=3, label="3h", step="hour", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        fig.show()


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password,) == hashed_text:
        return hashed_text
    return False


def add_userdata(name, email, username, password, password2):
    d = list(col2.find({"username": username},{"username":1,"_id":0}))
    print(d)
    if d:
        st.error("Username already exist, enter different username")


    else:
        col2.insert_one({"name": name, "email": email, "username": username, "password": password, "confirm_password": password2})
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")


def login_user(username, password):
    data = list(col2.find({"username": username, "password": password}))
    if data != None:
        return 1
    else:
        return 0


tickers = pd.read_html('https://ournifty.com/stock-list-in-nse-fo-futures-and-options.html#:~:text=NSE%20F%26O%20Stock%'
                       '20List%3A%20%20%20%20SL,%20%201000%20%2052%20more%20rows%20')[0]

tickers = tickers.SYMBOL.to_list()

for count in range(len(tickers)):
    tickers[count] = tickers[count] + ".NS"


def main():
    st.header("Stock Market Dashboard")
    menu = ["Home","Sign-in","Sign-up"]
    choice = st.sidebar.radio("STOCK DASHBOARD", menu)
    st.sidebar.form("abc")
    if choice == "Home":
        st.title("Home")
        st.info('What is the Stock Market?')
        st.write('The stock market refers to the collection of markets and exchanges'
                 ' where regular activities of buying, selling, and issuance of shares of publicly-held companies take place. '
                 'Such financial activities are conducted through institutionalized formal exchanges or over-the-counter (OTC) marketplaces '
                 'which operate under a defined set of regulations. '
                 'There can be multiple stock trading venues in a country or a region which allow transactions in stocks and other forms of securities.')
        img1 = Image.open("C:/Users/Sachet/Downloads/stock market dashboard/New folder/stockimage.jpg")
        st.image(img1, width=500)
        st.info('National Stock Exchange of India Limited (NSE)')
        #st.image(img,caption='NSE')
        st.write('National Stock Exchange of India Limited (NSE) is the leading government owned stock exchange of India,'
                 ' located in Mumbai, Maharashtra. It is under the ownership of Some leading financial institutions, '
                 'Banks and Insurance companies. NSE was established in 1992 as the first dematerialized electronic exchange in the country.'
                 ' NSE was the first exchange in the country to provide a modern, fully automated screen-based electronic '
                 'trading system that offered easy trading facilities to investors spread across the length and breadth of the country.'
                'Vikram Limaye is Managing Director & Chief Executive Officer of NSE.')
        st.write('National Stock Exchange has a total market capitalization of more than US$3 trillion, making it the world'
            '9th-largest stock exchange as of May 2021.NSE flagship index, the NIFTY 50, a 50 stock index is used '
            'extensively by investors in India and around the world as a barometer of the Indian capital market. '
            'The NIFTY 50 index was launched in 1996 by NSE.However,' 
            ' Vaidyanathan (2016) estimates that only about 4% of the Indian economy / GDP is actually derived from the stock exchanges in India.')
        st.info("Trading Schedule")
        st.write("Trading on the equities segment takes place on all days of the week (except Saturdays and Sundays and holidays declared by the Exchange in advance). "
                 "The market timings of the equities segment are:")
        st.markdown('(1) Pre-open session:')
        st.write('-Open Time: 09:00 hrs(9 am)')
        st.write('-Close Time: 17:00 hrs(5 pm)')
    if choice == "Sign-in":
        user = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            hashed_pswd = make_hashes(password)
            result = login_user(user, check_hashes(password, hashed_pswd))

            if result:
                st.success("Logged In as {}".format(user))
                menu2 = ["NIFTY Companies", "Graph", "Data frames", "Live Data"]
                ch = st.sidebar.radio("STOCK DASHBOARD", menu2)
                if ch == "NIFTY Companies":
                    l = ["NIFTY 50","All Stocks"]
                    ch = st.radio("NIFTY 50", l)
                    if ch == "NIFTY 50":
                        col = ["Company Name"]
                        df = pd.read_csv("ind_nifty50list.csv", usecols=col)
                        print(df["Company Name"])
                        st.table(df)
                    if ch == "All Stocks":
                        st.info("List of all 150 Comapnies ")
                        st.table(tickers)
                elif ch == "Live Data":
                    live_data()

                elif ch == "Graph":
                    coll1, coll2, coll3 = st.beta_columns(3)
                    with coll1:
                        stock_symbol = st.selectbox("Select company", tickers)
                    with coll2:
                        start_date = st.text_input("Start Date", "2014-1-1")
                    with coll3:
                        end_date = st.text_input("End Date", datetime.date.today())

                    data = yf.download(stock_symbol, start=start_date,
                                       end=end_date)

                    st.line_chart(data['Open'])
                    st.line_chart(data['Close'])

                    chardata1 = pd.DataFrame(data, columns=['Open', 'Close'])
                    st.line_chart(chardata1)

                    st.line_chart(data['High'])
                    st.line_chart(data['Low'])

                    chardata2 = pd.DataFrame(data, columns=['High', 'Low'])
                    st.line_chart(chardata2)

                elif ch == "Data frames":
                    col1, col2, col3 = st.beta_columns(3)
                    with col1:
                        stock_symbol2 = st.selectbox("Select company", tickers)
                    with col2:
                        start_date2 = st.text_input("Start Date", "2014-1-1")
                    with col3:
                        end_date2 = st.text_input("End Date", datetime.date.today())

                    data2 = yf.download(stock_symbol2, start=start_date2,
                                       end=end_date2)
                    st.table(data2)
            else:
                st.sidebar.error("Invalid")
                
    elif choice == "Sign-up":
        st.subheader("Create New Account")
        name = st.text_input("Name")
        email = st.text_input("Email")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        new_password2 = st.text_input("Confirm Password", type='password')
        if st.button("Signup"):
            if new_password != new_password2:
                st.sidebar.error("Passwords do not match")
            elif name == "" and  email == "" and new_user == "":
                st.sidebar.error("enter the fields")
            else:
                add_userdata(name, email, new_user, make_hashes(new_password), make_hashes(new_password2))


if __name__ == '__main__':
    main()