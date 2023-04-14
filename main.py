import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
load_dotenv()

STOCK_APY_KEY = os.environ.get('STOCKS_API_KEY')
stock_endpoint = 'https://www.alphavantage.co/query'
stock_parameters = {
    'function' : 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol' : STOCK,
    'apikey' : STOCK_APY_KEY
}

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
news_endpoint = 'https://newsapi.org/v2/everything'
news_parameters = {
    'apiKey' : NEWS_API_KEY,
    'q' : COMPANY_NAME,
    'language' : 'en'
}

account_sid = os.environ.get('SID')
auth_token = os.environ.get('AUTH_TOKEN')

stock_response = requests.get(stock_endpoint, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()['Time Series (Daily)']
key_list = list(stock_data.keys())
yesterday = float(stock_data[key_list[0]]['4. close'])
before_yesterday = float(stock_data[key_list[1]]['4. close'])
percentage_difference = round(((yesterday - before_yesterday)/yesterday)*100)
up_down = None
if percentage_difference > 0:
    up_down= '🔺'
else:
    up_down = '🔻'

if abs(percentage_difference) > 2:
    news_response = requests.get(news_endpoint, params=news_parameters)
    news_response.raise_for_status()
    articles = news_response.json()['articles']
    three_first_articles = articles[:3]
    sms_content = [f"{STOCK}: {up_down}{percentage_difference}%\nHeadline: {article['title']}. \nDescription: {article['description']}" for article in three_first_articles]
    print(sms_content)
    client = Client(account_sid, auth_token)
    for article in sms_content:
        message = client.messages.create(
        body=article,
        from_="+15074456521",
        to="+5584999533866"
    )
