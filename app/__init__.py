from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Config import config
from ariadne.constants import PLAYGROUND_HTML

from flask import request, jsonify


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:postgres@{config.host}:5432/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
mas = Marshmallow(app)


