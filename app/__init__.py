from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .sync import sync
import os

app = Flask(__name__)    #creates our app

BASE_DIR=os.path.dirname(os.path.realpath(__file__))                #finds the path to the db
connection_string="sqlite:///"+os.path.join(BASE_DIR,'barbot.db')   

#put flask config here alternativly create a config file

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string        #tells where  db is 
app.config["SECRET_KEY"] = '571ebf8e13ca209536c29be68d435c00'    #secret key that may be needed for certain flask functions
 
db = SQLAlchemy(app)        #creates the Database


from app import control_views  #List all files that are used in flask app 
from app import admin_views
from app import views
from app import models

sync()
