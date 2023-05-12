import requests
import csv
from secret import API_KEY

def intra_day_data(ticker, howlonggo):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={ticker}&interval=15min&slice=year1month1&apikey={API_KEY}'

    response = requests.get(url)
    decoded_content = response.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)

    latest_date = max([item[0].split()[0] for item in my_list[1:]])
    dates = sorted(list(set([item[0].split()[0] for item in my_list[1:]])), reverse=True)
    x_latest_date = dates[int(howlonggo) - 1]

    stock = [item for item in my_list[1:] if x_latest_date <= item[0].split()[0] <= latest_date]

    return [stock, latest_date]