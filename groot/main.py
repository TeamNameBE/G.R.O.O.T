import tensorflow as tf
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import sys


def main(argv):
    if len(argv) == 0:
        print("You must speciifie number of train or a model to load")

    if argv[0].isdigit(): # phase de train on va recréer un model

        nb_train = int(argv[0])

        mnist = tf.keras.datasets.mnist
        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        x_train = tf.keras.utils.normalize(x_train, axis=1)
        x_test = tf.keras.utils.normalize(x_test, axis=1)

        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
        model.add(tf.keras.layers.Dense(units=512, activation=tf.nn.relu))
        model.add(tf.keras.layers.Dense(units=258, activation=tf.nn.relu))
        model.add(tf.keras.layers.Dense(units=126, activation=tf.nn.relu))
        model.add(tf.keras.layers.Dense(units=10, activation=tf.nn.softmax))

        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        model.fit(x_train, y_train, epochs=nb_train)

        loss, accuracy = model.evaluate(x_test, y_test)

        print(accuracy)
        print(loss)

        model.save("digit.model")

    else:  # phase de test on load un model

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
            filename = input("enter filename of picture ")


if __name__ == "__main__":
    main(sys.argv[1:])
