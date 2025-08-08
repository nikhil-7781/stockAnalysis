import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, start_date, end_date):
    if not ticker.endswith('.NS'):
        ticker += '.NS'
    data = yf.download(ticker, start=start_date, end=end_date)
    return data[['Open', 'High', 'Low', 'Close', 'Volume']]
