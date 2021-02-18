import os

# Contains the settings of the groot website

UPLOAD_FOLDER = "static/media/"
ALLOWED_EXTENSIONS = set([".png", ".jpg", ".jpeg"])
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
