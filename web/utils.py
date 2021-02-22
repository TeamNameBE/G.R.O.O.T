import os

from settings import ALLOWED_EXTENSIONS


def allowed_file(filename):
    """
    Return true if the filename as an authorized extension
    """
    return get_extension(filename) in ALLOWED_EXTENSIONS


def get_extension(filename):
    return os.path.splitext(filename)[1]


def get_job_position(job, nb_job, conn):
    for x in range(nb_job):
        if conn.lindex("job", x).decode() == job:
            return x
    return -1
