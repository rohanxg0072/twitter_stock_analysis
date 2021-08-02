from flask import render_template, url_for, flash, redirect, request, Blueprint
from flasksite.twitter.forms import StockForm
import yfinance as yf
from flasksite.twitter.utils import get_prices, get_sentiments_times, get_chart_url, getShortName
from quickchart import QuickChart

twitter = Blueprint("twitter", __name__)

@twitter.route("/", methods=["GET", "POST"])
@twitter.route("/twitter", methods=["GET", "POST"])
def twitter_chart():

    form = StockForm()
    if form.validate_on_submit():
        sentiments_times = get_sentiments_times(form.stock.data)   
        prices = get_prices(sentiments_times[1], (form.stock.data))
        dates = []
        for time in sentiments_times[1]:
                dates.append(time[0:10])

        sentiments = sentiments_times[0]
        chart_url = get_chart_url(dates, prices, sentiments, form.stock.data)
        return render_template("twitter.html", form = form, chart_url = chart_url) 

    return render_template("twitter.html", form = form)