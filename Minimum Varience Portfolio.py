import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as BS
from matplotlib import pyplot as plt
from datetime import datetime
import fake_useragent as orange
import datetime
np.random.seed(7512)

dataframe = pd.read_excel(r'C:\Users\Dell\Desktop\Rooster Logic\GVMP_trial\GVMP.xlsx',index_col='Date')
# dataframe['Date'] = pd.to_datetime(dataframe['Date'])
dataframe.index = pd.to_datetime(dataframe.index)
returns_daily = dataframe.pct_change()
returns_daily=returns_daily.dropna()
returns_annual = returns_daily.mean() #mean of daily returns
std_of_each_anual = returns_daily.std()
variance_of_each_annual = std_of_each_anual**2
number_of_days = len(returns_daily['M&M'])
cov_daily=returns_daily.cov()
cov_annual = cov_daily * len(returns_daily)
port_returns = []
port_volatility = []
stock_weights = []
num_assets = len(returns_daily.columns)
num_portfolios = 100000

# populate the empty lists with each portfolios returns,risk and weights
for single_portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    returns = np.dot(weights, returns_annual)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
    port_returns.append(returns)
    port_volatility.append(volatility)
    stock_weights.append(weights)
portfolio = {'Returns': port_returns,
             'Volatility': port_volatility}
for counter, symbol in enumerate(returns_daily.columns):
    portfolio[symbol + ' Weight'] = [Weight[counter] for Weight in stock_weights]
df = pd.DataFrame(portfolio)
column_order = ['Returns', 'Volatility'] + [stock + ' Weight' for stock in returns_daily.columns]
df = df[column_order]
min_volatility = df['Volatility'].min()
min_variance_port = df.loc[df['Volatility'] == min_volatility]

#this file is exactly as sir sent. The only difference is that sir's file has it in % and this is absolute
