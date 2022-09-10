import streamlit as st
import pandas as pd
from PIL import Image

st.write ("""
# Stock Market Web Application
**Visually** show data on a stock! Data range from Jan 2, 2020 - Aug 4, 2020
""")

image = Image.open("/Users/ashleigh/Downloads/stonk_img.png")
st.image(image, use_column_width=True)

#create a sidebar header
st.sidebar.header('User Input')

#create fcn to get the user's input from
def get_input():
    start_date=st.sidebar.text_input("Start Date", "2020-01-02")
    end_date=st.sidebar.text_input("End Date", "2020-08-04")
    stock_symbol=st.sidebar.text_input("Stock Symbol", "AMZN")
    return start_date, end_date, stock_symbol

#create fcn to get the company name
def get_company_name(symbol):
    if symbol == "AMZN":
        return 'Amazon'
    elif symbol == 'TSLA':
        return 'Tesla'
    elif symbol == 'GOOG':
        return 'Alphabet'
    else:
        'None'
        
#create a fcn to get the proper company data and the proper timeframe from the user's start date to the user's end date
def get_data(symbol, start, end):
    #load the Data
    if symbol.upper()=='AMZN':
        df = pd.read_csv("/Users/ashleigh/Desktop/side projects/stock predictor/AMZN.csv")
    elif symbol.upper()=='TSLA':
        df = pd.read_csv("/Users/ashleigh/Desktop/side projects/stock predictor/TSLA.csv")
    elif symbol.upper()=='GOOG':
        df = pd.read_csv("/Users/ashleigh/Desktop/side projects/stock predictor/GOOG.csv")
    else:
        df= pd.DataFrame(columns = ['Date', 'Close', 'Open', 'Volume', 'Adj Close', 'High', 'Low'])
        
    #get the date range
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    
    #set the start and end index rows both to 0
    start_row = 0
    end_row = 0
    
    #start the date from the top of the data set and go down to see if the users start date is less than or equal to the date in the data set
    for i in range (0, len(df)):
        if start <= pd.to_datetime(df['Date'][i]):
            start_row = i
            break
    
    #start from the bottom of the data set and go up to see if the users end date is greater than or equal to the date in the data set
    for j in range (0, len(df)):
        if end>= pd.to_datetime(df['Date'][len(df)-1-j]):
            end_row = len(df) - 1 - j
            break
        
    #set the index to be the date
    df = df.set_index(pd.DatetimeIndex(df['Date'].values))
    
    return df.iloc[start_row:end_row +1, :]

#get the users Input
start, end, symbol = get_input()

#get the data
df = get_data(symbol, start, end)

#get the company name
company_name = get_company_name(symbol.upper())

#display the close price
st.header(company_name+" Close Price\n")
st.line_chart(df['Close'])

#display the Volume
st.header(company_name+" Volume\n")
st.line_chart(df['Volume'])

#get statistics on the data
st.header('Data Statistics')
st.write(df.describe())