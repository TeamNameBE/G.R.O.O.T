import tensorflow as tf


def train(nb_train=500):
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


if __name__ == "__main__":
    train()
