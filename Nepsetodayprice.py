import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as BS
from matplotlib import pyplot as plt
from datetime import datetime
import fake_useragent as orange
import datetime

np.random.seed(974)
Riskfreerate = 0.045730

# I tried doing this by Get method but this website uses POST method
# Firefox inspector- network- post-Params and response

start = datetime.datetime.strptime("2015-12-19", "%Y-%m-%d").date()
end = datetime.datetime.strptime("2016-05-29", "%Y-%m-%d").date()
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
numberofdays = np.busday_count(start, end, weekmask=[1, 1, 1, 1, 0, 0, 1])

stock_symbol = ['NABIL', 'NIB']
all_rows1 = []
all_headings1 = ['S.N', 'Traded_Companies', 'Number_of_transactions', 'Max_Price', 'Min_Price', 'Closing_Price',
                 'Traded_Shares', 'Amount', 'Previous_Closing', 'Difference']
nepse_todayprice1 = pd.DataFrame(columns=all_headings1)
for dater in date_generated:
    try:
        UURL = 'http://www.nepalstock.com/main/todays_price'
        data = {'startDate': dater, 'stock-symbol': '', '_limit': '1000'}

        requesting = requests.post(UURL, data=data, headers=orange.random_headers())

        souped = BS(requesting.content, 'html.parser')
        # to get the table
        table = souped.find('tbody')

        # to get the table rows
        table_rows = souped.find_all('tr')

        all_headings = ['S.N', 'Traded_Companies', 'Number_of_transactions', 'Max_Price', 'Min_Price',
                        'Closing_Price',
                        'Traded_Shares', 'Amount', 'Previous_Closing', 'Difference']
        all_rows = []
        for index, single_row in enumerate(table_rows):
            #         # we are not taking the below mentioned index cause there are additional information there and we dont want that
            if index != 0 and index != 1:
                table_data = single_row.find_all('td')
                single_row_data = [i.text.strip() for i in table_data]
                all_rows.append(single_row_data)
                all_rows1.append(all_rows)

        nepse_todayprice = pd.DataFrame()
        nepse_todayprice = pd.DataFrame(all_rows, columns=all_headings)
        nepse_todayprice.set_index('S.N', inplace=True)
        nepse_todayprice = nepse_todayprice[:-4]
        dateToBeInput = souped.find(class_='pull-left').text.strip()[6:16]
        nepse_todayprice['Date'] = dateToBeInput
        nepse_todayprice = nepse_todayprice.set_index('Date')
        nepse_todayprice1 = nepse_todayprice1.append(nepse_todayprice, sort=True)
        nepse_todayprice1 = nepse_todayprice1[
            ['Traded_Companies', 'Number_of_transactions', 'Max_Price', 'Min_Price', 'Closing_Price',
             'Traded_Shares', 'Amount', 'Previous_Closing', 'Difference', 'Date']]


    except:
        pass
nepse_todayprice1.to_csv(r'C:\Users\Dell\Anaconda3\Nepse_Scraping_till_retreiving_from_mongo\allnepseprice.csv')
