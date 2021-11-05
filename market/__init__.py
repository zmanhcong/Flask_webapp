from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'fb8565bbd6c7c6dd5eaa6592' #crete key by cmd: uramndom(12).hex() #app.config is config key name and create market.db::: SQLALCHEMY_DATABASE_URI: is key name
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"               #Not loggin yet, must loggin first.
login_manager.login_message_category = "info"         #make color for message: Please log in to access this page.
from market import routes
#use this stament for connect with routes.
#app.config is config key name and create market.db::: SQLALCHEMY_DATABASE_URI: is key name

