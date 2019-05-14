from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from helpers import mapperfunc

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Bigboy1294@localhost/flasktrails'
#db = SQLAlchemy(app)

#from models import 


@app.route("/")
def index:
    return 'index.html'
