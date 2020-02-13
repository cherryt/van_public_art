from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config


app = Flask(__name__)
load_dotenv()
app.config.from_object(Config)
db = SQLAlchemy(app)

import van_public_art.views  # noqa
