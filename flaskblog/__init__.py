from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e1a40d7a2efd062b4c7caee4499a56aa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Import models after db is created to avoid circular imports
from flaskblog import models

# Set up user_loader after models are imported
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

from flaskblog import routes
