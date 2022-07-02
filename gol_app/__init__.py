from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = "some_super_secret_password"
app.config['DEBUG'] = False

db_info = {
    'host': 'localhost',
    'database': 'hackaton-2',
    'psw': 'learningSQL',
    'user': 'postgres',
    'port': ''
}

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://" \
                                        f"{db_info['user']}:" \
                                        f"{db_info['psw']}@" \
                                        f"{db_info['host']}/" \
                                        f"{db_info['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

file = open('gol_app/templates/index.html')

from gol_app import models, routes