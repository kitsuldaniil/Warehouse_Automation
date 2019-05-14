from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
# application.config.from_object('config')
app.secret_key = 'A1hr97j/3yX R~XHY!jmN]LWX/,?RT'
app.config.from_object(Config)
db = SQLAlchemy(app)

# code


# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()
