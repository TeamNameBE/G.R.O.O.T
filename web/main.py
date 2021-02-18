import os
import secrets

import redis
from flask import Flask, flash, redirect, render_template, request, url_for

from settings import UPLOAD_FOLDER, REDIS_HOST
from utils import allowed_file, get_extension

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "vairysekrette")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ia", methods=["GET", "POST"])
def ia_home():
    if request.method == "GET":
        return render_template("ia.html")

    if "file" not in request.files:
        flash("Aucun fichier n'a été fourni")
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "":
        flash("Aucune image n'a été envoyée")
        return redirect(request.url)

    if allowed_file(file.filename):
        database = redis.Redis(host=REDIS_HOST, port=6379, db=0)

        ext = get_extension(file.filename)
        filename = secrets.token_hex(6)
        while database.get(filename) is not None:
            filename = secrets.token_hex(6)

        filename_full = "{}{}".format(filename, ext)

        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename_full))
        database.set(f"{filename}_photo", filename_full)
        database.lpush("job", filename)
        return redirect(f"/results?job={filename}")

    else:
        flash("Allowed image types are -> png, jpg, jpeg")
        return redirect(request.url)


@app.route("/results", methods=["GET"])
def results_view():
    filename = request.args.get("job", None)
    if filename is None or filename == "":
        return redirect("/")
    return render_template("waiting-screen.html", filename=filename)


@app.route("/display/<filename>")
def display_image(filename):
    database = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    filename_full = database.get(filename)
    if filename_full is None:
        return redirect(url_for("static", filename="img/404.gif"), code=301)
    return redirect(
        url_for("static", filename="media/" + filename_full.decode()), code=301
    )


if __name__ == "__main__":
    app.run(debug=True)
