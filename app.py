from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from helpers import mapperfunc

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/flasktrails'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jqewotptknoxrj:54ea7f064f3ea562961843cf894e446774889fece265324e8b4e6ab7e3278ab6@ec2-54-163-226-238.compute-1.amazonaws.com:5432/d3jtih4nl7s405'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




@app.route("/")
def index():
    return 'index.html'
