import json
import yfinance as yf
from datetime import datetime, timedelta
import requests
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from quickchart import QuickChart

def go_back_days(now, days, dtformat = '%Y-%m-%dT%H:%M:%SZ'):
    now = datetime.strptime(now, dtformat)
    back_in_time = now - timedelta(days=days)
    return back_in_time.strftime(dtformat)

def get_sentiments_times(ticker):
        BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAA7uSAEAAAAAwYwVJQ4rEPJ7WOLfAIxtowmzozY%3DYOQcDP1Lsjb3BgmKCpUfvAiJLYILIcF1GcUXuRewg7bPplv2Wl"

        endpoint = 'https://api.twitter.com/2/tweets/search/recent'
        headers = {'authorization': f'Bearer {BEARER_TOKEN}'}
        params = {
        'query': f'({ticker}) (lang:en)',
        'max_results': '10',
        'tweet.fields': 'created_at,lang',
        }

        dtformat = '%Y-%m-%dT%H:%M:%SZ'

        now = datetime.now().replace(hour = 13, minute= 30, second=0)
        now = go_back_days(now.strftime(dtformat), 1)

        avgSentiment = []
        times = []

        for x in range(0, 5):
                day_before = go_back_days(now, 1)
                
                params['start_time'] = day_before
                params['end_time'] = now

                times.append(now)

                response = requests.get(endpoint,
                                params=params,
                                headers=headers)
                now = day_before
                        
                tweets = 0
                totalSentiment = 0
                sid = SentimentIntensityAnalyzer()

                for tweet in response.json()['data']:
                        totalSentiment += sid.polarity_scores(tweet['text'])["compound"]
                        tweets += 1

                avgSentiment.append(totalSentiment/tweets)
                
        avgSentiment.reverse()
        times.reverse()

        return([avgSentiment, times])

def get_prices(times, ticker):
    prices = []
    stock = yf.Ticker(ticker)
    for time in times:
        price = stock.history(
        start = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ'),
        end = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
        )
        prices.append(price["Open"][0])

    return prices

def get_chart_url(dates, prices, sentiments, ticker):
    name = getShortName(ticker)
    title = f'Twitter Sentiment Analysis for {name}'

    qc = QuickChart()

    qc.width = 1000
    qc.height = 600
    qc.config = {
        "type": "line",
        "data": {
        "labels": dates,
        "datasets": [
      {
        "label": "Twitter Sentiment",
        "borderColor": "rgb(54, 162, 235)",
        "backgroundColor": "rgb(54, 162, 235)",
        "fill": False,
        "data": sentiments,
        "yAxisID": "y"
      },
      {
        "label": "Stock Price",
        "borderColor": "rgb(255, 99, 132)",
        "backgroundColor": "rgb(255, 99, 132)",
        "fill": False,
        "data": prices,
        "yAxisID": "y1"
      }
    ]
    },
    "options": {
        "stacked": False,
        "title": {
        "display": True,
        "text": title
        },
        "scales": {
        "yAxes": [
        {
            "id": "y",
            "type": "linear",
            "display": True,
            "position": "left"
        }, 
        {
            "id": "y1",
            "type": "linear",
            "display": True,
            "position": "right",
            "gridLines": {
            "drawOnChartArea": False
            }
        }
        ]
        }
    }
    }

    return qc.get_url()


# useful to include in twitter API query if using larger number of tweets
def getShortName(ticker):
        with open("stocks.json") as file:
                stocks_dicts = json.load(file)
                for dict in stocks_dicts:
                        try:
                                if(dict["ACT Symbol"] == ticker.upper()):
                                        stock = dict
                        except KeyError:
                                if(dict["Symbol"] == ticker.upper()):
                                        stock = dict

        shortName = stock["Company Name"]

        if(stock["Company Name"].find(",") > 0):
                shortName = stock["Company Name"][0: stock["Company Name"].find(",")]                
        if(shortName.lower().find(" inc") > 0):
                shortName = shortName[0: shortName.lower().find(" inc")]
        if(shortName.lower().find(" ltd") > 0):
                shortName = shortName[0: shortName.lower().find(" ltd")]
        if(shortName.lower().find(" plc") > 0):
                shortName = shortName[0: shortName.lower().find(" plc")]
        if(shortName.lower().find(" sa") > 0):
                shortName = shortName[0: shortName.lower().find(" sa")]
        if(shortName.lower().find(" nv") > 0):
                shortName = shortName[0: shortName.lower().find(" nv")]
        if(shortName.lower().find(" (") > 0):
                shortName = shortName[0: shortName.lower().find(" (")]
        if(shortName.lower().find(" company") > 0):
                shortName = shortName[0: shortName.lower().find(" company")]
        if(shortName.lower().find(" corporation") > 0):
                shortName = shortName[0: shortName.lower().find(" corporation")]
        if(shortName.lower().find(" corp.") > 0):
                shortName = shortName[0: shortName.lower().find(" corp.")]
        if(shortName.lower().find(" -") > 0):
                shortName = shortName[0: shortName.lower().find(" -")]

        return shortName
