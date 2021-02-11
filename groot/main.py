import tensorflow as tf
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
# import redis


def main(argv):
    # database = redis.Redis(host='localhost', port=6379, db=0)
    model_name = argv[0]

    model = tf.keras.models.load_model(model_name)

    filename = input("enter filename of picture ")
    while filename != "quit":
        img = cv.imread(filename)[:, :, 0]
        img = cv.resize(img, (28, 28))
        img = np.invert(np.array([img]))
        prediction = model.predict(img)
        print(np.argmax(prediction))
        plt.imshow(img[0], cmap=plt.cm.binary)
        plt.show()
        filename = input("enter filename of picture")


if __name__ == "__main__":
    main()
