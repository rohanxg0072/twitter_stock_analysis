'''
Create flask app and SQL database here
'''
from os import error
from flask import Flask, config
from flask_bootstrap import Bootstrap
from flasksite.config import Config


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from flasksite.twitter.routes import twitter
from flasksite.main.routes import main
from flasksite.errors.handlers import errors

app.register_blueprint(twitter)
app.register_blueprint(main)
app.register_blueprint(errors)


