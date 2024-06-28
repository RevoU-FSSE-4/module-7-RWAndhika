from flask import Flask
from dotenv import load_dotenv
from connectors.mysql_connector import connection

from sqlalchemy.orm import sessionmaker

from controllers.user import user_routes
from controllers.review import review_routes
import os

from flask_login import LoginManager
from models.user import User

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(user_routes)
app.register_blueprint(review_routes)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    Session = sessionmaker(connection)
    s = Session()
    return s.query(User).get(int(user_id))

@app.route("/")
def hello_world():
    return "Hello World"