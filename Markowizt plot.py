import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as BS
from matplotlib import pyplot as plt
from datetime import datetime
import fake_useragent as orange
import datetime
from Nepsetodayprice import numberofdays as numberofdays

np.random.seed(7512)
Riskfreerate = 0.0458
####################
clean_nepse_todayprice = pd.DataFrame(
    pd.read_csv(r'C:\Users\Dell\Anaconda3\Nepse_Scraping_till_retreiving_from_mongo\allnepseprice.csv'))
nepse_newtoday = clean_nepse_todayprice[['Traded_Companies', 'Closing_Price']]
nepse_newtoday['Closing_Price'] = nepse_newtoday['Closing_Price'].astype(float)
# nepse_newtoday = nepse_newtoday[(nepse_newtoday['Traded_Companies']=='11% NIC Asia Debenture 082/83') | (nepse_newtoday['Traded_Companies']=='Agriculture Development Bank Limited')]
# nepse_newtoday = nepse_newtoday[(nepse_newtoday['Traded_Companies']!='11% NIC Asia Debenture 082/83')]
nepse_newtoday = nepse_newtoday[(nepse_newtoday['Traded_Companies'] == 'Nabil Bank Limited')
                                | (nepse_newtoday['Traded_Companies'] == 'Nepal Investment Bank Limited')
                                | (nepse_newtoday['Traded_Companies'] == 'Sanima Bank Limited')
                                | (nepse_newtoday['Traded_Companies'] == 'Kumari Bank Limited')]
tablee = nepse_newtoday.pivot(columns='Traded_Companies')
returns_daily = tablee.pct_change()
returns_annual = returns_daily.mean() * numberofdays
# get daily and covariance of returns of the stock
cov_daily = returns_daily.cov()
cov_annual = cov_daily * numberofdays
selected = ['Nabil Bank Limited', 'Nepal Investment Bank Limited',
            'Kumari Bank Limited', 'Sanima Bank Limited']
# empty lists to store returns, volatility and weights of imiginary portfolios
port_returns = []
sharpe_ratio = []
port_volatility = []
stock_weights = []
# set the number of combinations for imaginary portfolios
num_assets = len(selected)
num_portfolios = 100000

# populate the empty lists with each portfolios returns,risk and weights
for single_portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    returns = np.dot(weights, returns_annual)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
    sharpe = (returns - Riskfreerate) / volatility
    sharpe_ratio.append(sharpe)
    port_returns.append(returns)
    port_volatility.append(volatility)
    stock_weights.append(weights)

# a dictionary for Returns and Risk values of each portfolio
portfolio = {'Returns': port_returns,
             'Volatility': port_volatility,
             'Sharpe Ratio': sharpe_ratio
             }

# extend original dictionary to accomodate each ticker and weight in the portfolio
for counter, symbol in enumerate(selected):
    portfolio[symbol + ' Weight'] = [Weight[counter] for Weight in stock_weights]
# make a nice dataframe of the extended dictionary
df = pd.DataFrame(portfolio)

# get better labels for desired arrangement of columns
column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock + ' Weight' for stock in selected]

# reorder dataframe columns
df = df[column_order]

# find min Volatility & max sharpe values in the dataframe (df)
min_volatility = df['Volatility'].min()
max_sharpe = df['Sharpe Ratio'].max()

# use the min, max values to locate and create the two special portfolios
sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
min_variance_port = df.loc[df['Volatility'] == min_volatility]

# Find the Capital Allocation Line
# CAL = (((0.056-Riskfreerate)/volatility)*0.053289)+Riskfreerate

# plot frontier, max sharpe & min Volatility values with a scatterplot
plt.style.use('seaborn-dark')
df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='red', s=10)
plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='blue', s=10)
for_YaxisCAL = [Riskfreerate, 0.120931]
for_XaxisCAL = [0, 0.04813]
plt.plot(for_XaxisCAL, for_YaxisCAL, lw=0.5)
plt.axvline(x=0.024919, color='red')
plt.plot()
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')
plt.savefig(r'C:\Users\Dell\Anaconda3\Nepse_Scraping_till_retreiving_from_mongo\Markowitz_Efficientwkumaribank2.png')
# print the details of the 2 special portfolios
print(min_variance_port.T)
print(sharpe_portfolio.T)
