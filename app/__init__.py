from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "unsia_uas_pl_sql"
app.config.from_object('config.Config')
db = SQLAlchemy(app)

from app.routes import customer
from app.routes import merchant
from app.routes import payment
from app.routes import log

