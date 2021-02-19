import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

import redis
import json


def load_settings():
    f = open("settings.json")
    return json.load(f)


def main():
    settings = load_settings()
    database = redis.Redis(host=settings["db_host"], port=6379, db=0)

    while True:
        # * Waits until a job is pushed to the "job" list
        _, job_id = database.brpop("job")
        os.sleep(2)  # ! Make sure the entry has been set

        img_name = database.get(f"{job_id}_photo")
        img_path = f"{settings['media_dir']}/{img_name}"

        model = keras.models.load_model(settings["model_name"])

        img = keras.preprocessing.image.load_img(
            img_path, target_size=(settings["img_height"], settings["img_width"])
        )
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create a batch

        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        database.set(
            f"{job_id}_result",
            "This image most likely belongs to {} with a {:.2f} percent confidence.".format(
                settings["class_names"][np.argmax(score)], 100 * np.max(score)
            ),
        )

    """
    filename = input("enter filename of picture ")
    while filename != "quit":
        img = cv.imread(filename)[:, :, 0]
        img = cv.resize(img, (img_height, img_weight))

        h, w = img.shape
        if h > w:
            middle = (h - w)//2
            img = img[middle:w+middle, 0:w]
        else:
            middle = (w - h)//2
            img = img[0:h, middle:h+middle]

        img_array = tf.keras.preprocessing.image.img_to_array(img)
        prediction = model.predict(img_array)
        print(np.argmax(prediction))
        plt.imshow(img[0], cmap=plt.cm.binary)
        plt.show()
        filename = input("enter filename of picture")
    """


if __name__ == "__main__":
    main()
