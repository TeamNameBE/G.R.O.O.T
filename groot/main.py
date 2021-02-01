import tensorflow as tf
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

"""mnist = tf.keras.datasets.mnist
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

model.fit(x_train, y_train, epochs=5)

loss, accuracy = model.evaluate(x_test, y_test)

print(accuracy)
print(loss)
"""
model = tf.keras.models.load_model("digit.model")

filename = input("enter filename of picture ")
while filename != "quit":
    img = cv.imread(filename)[:, :, 0]
    img = np.invert(np.array([img]))
    prediction = model.predict(img)
    print(np.argmax(prediction))
    plt.imshow(img[0], cmap=plt.cm.binary)
    plt.show()
    filename = input("enter filename of picture ")