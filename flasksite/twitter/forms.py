import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import yfinance as yf

class StockForm(FlaskForm):
    tickers_list =[]
    with open("stock_tickers.txt") as tickers_file:
        tickers = tickers_file.readlines()
        for ticker in tickers:
            tickers_list.append(ticker[0:len(ticker)-1])

    stock = StringField("Enter a Stock Ticker:", validators=[DataRequired()])
    submit = SubmitField("Enter")

    def validate_stock(self, stock, tickers_list=tickers_list):
        '''
        Less efficient ways of checking if ticker is valid

        with open("stocks.json") as file:
            tickers = json.load(file)
            tickers_list =[]
            for entry in tickers:
                if("ACT Symbol" in entry):
                    tickers_list.append(entry["ACT Symbol"])
                elif("Symbol" in entry):
                    tickers_list.append(entry["Symbol"])
        '''
        if(not(stock.data.upper() in tickers_list)):
            raise ValidationError(f'"{stock.data.upper()}" is not a valid NYSE or Nasdaq listed stock ticker.')
        