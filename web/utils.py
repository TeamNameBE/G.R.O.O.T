import os

from settings import ALLOWED_EXTENSIONS


def allowed_file(filename):
    """
        Return true if the filename as an authorized extension
    """
    return get_extension(filename) in ALLOWED_EXTENSIONS


def get_extension(filename):
    return os.path.splitext(filename)[1]
