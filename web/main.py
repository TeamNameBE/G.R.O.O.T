import os
import secrets
from twython import Twython

import redis
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify

from settings import UPLOAD_FOLDER, REDIS_HOST
from utils import allowed_file, get_extension, get_job_position

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

    database = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    job_done = database.get(f"{filename}_result") is not None
    context = {"job_done": job_done, "job_id": filename}

    if job_done:
        context.update(
            {
                "result_family": database.get(f"{filename}_result_family").decode(),
                "result_confidence": database.get(f"{filename}_result_perc").decode(),
            }
        )
    else:
        nb_jobs = database.llen("job")
        context.update(
            {
                "nb_jobs": nb_jobs,
                "job_position": nb_jobs - get_job_position(filename, nb_jobs, database),
            }
        )

    return render_template("waiting-screen.html", filename=filename, context=context)


@app.route("/display/<filename>")
def display_image(filename):
    database = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    filename_full = database.get(f"{filename}_photo")
    if filename_full is None:
        return redirect(url_for("static", filename="img/404.gif"), code=301)
    return redirect(
        url_for("static", filename="media/" + filename_full.decode()), code=301
    )


@app.route("/api/result", methods=["GET"])
def api_result():
    database = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    job_id = request.args.get("job", None)
    if job_id is None:
        return jsonify({"status": "error", "error": "no job specified"})

    job_done = database.get(f"{job_id}_result") is not None
    if job_done:
        return jsonify(
            {
                "status": "done",
                "result": {
                    "family": database.get(f"{job_id}_result_family").decode(),
                    "confidence": database.get(f"{job_id}_result_perc").decode(),
                },
            }
        )

    nb_jobs = database.llen("job")
    position = get_job_position(job_id, nb_jobs, database)

    return jsonify({"status": "running", "position": position, "running_jobs": nb_jobs})


@app.route("/tweet", methods=["GET"])
def tweet_result():
    job_id = request.args.get("job", None)
    if job_id is None:
        flash("Vous ne pouvez pas acceder à cette page sans job_id")
        return redirect("/")

    database = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    if database.get(f"{job_id}_tweet") is not None:
        flash("Ce résultat à déjà été tweeté !")
        return redirect("/")

    CONSUMER_KEY = os.environ.get("CONSUMER_KEY", "SUPERSECRET")
    CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET", "YOULLNEVERFIND")
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "WELLATLEASTYOUTRIED")
    ACCESS_SECRET = os.environ.get("ACCESS_SECRET", "NOPENOTTHISONE")

    filename = database.get(f"{job_id}_photo").decode()
    family = database.get(f"{job_id}_result_family").decode()
    confidence = database.get(f"{job_id}_result_perc").decode()

    database.set(f"{job_id}_tweet", "true")
    text = f"Cette plante appartient à la famille {family} (confiance : {confidence}) \n #Groot https://groot.ninja"

    photo = open(os.path.join(app.config["UPLOAD_FOLDER"], filename), "rb")
    api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

    response = api.upload_media(media=photo)
    response = api.update_status(status=text, media_ids=[response["media_id"]])
    return redirect(response["entities"]["urls"][0]["url"])


if __name__ == "__main__":
    app.run(debug=True)
