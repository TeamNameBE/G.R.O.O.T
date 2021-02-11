import os
import secrets

import redis
from flask import Flask, flash, redirect, render_template, request, url_for

from settings import UPLOAD_FOLDER, EXTENSIONS_VALUES
from utils import allowed_file, get_extension

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "vairysekrette")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ia')
def ia_home():
    return render_template('ia.html')


if __name__ == "__main__":
    app.run(debug=True)
