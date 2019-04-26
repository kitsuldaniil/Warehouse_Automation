from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from app import config

app = Flask(__name__)
app.secret_key = 'A1hr97j/3yX R~XHY!jmN]LWX/,?RT'
#app.config.from_object(config.Config)
db = SQLAlchemy(app)
