import tensorflow as tf
from tensorflow.keras import layers
import sys
import matplotlib.pyplot as plt
import json


def load_settings():
    f = open("settings.json")
    return json.load(f)


def train(argv):

    settings = load_settings()
    nb_train = int(argv[0])
    batch_size = 32
    img_height = settings["img_height"]
    img_width = settings["img_width"]

    train_directory = "data/flowers/train"
    val_directory = "data/flowers/val"

    physical_devices = tf.config.list_physical_devices("GPU")
    try:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
    except Exception as e:
        print(f"\n\n COULD NOT SET MEMORY GROWTH TRUE : {e} \n\n")
        # Invalid device or cannot modify virtual devices once initialized.
        pass

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        train_directory,
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size,
    )

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        val_directory,
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size,
    )

    num_class = len(train_ds.class_names)

    AUTOTUNE = tf.data.experimental.AUTOTUNE

    train_ds = (
        train_ds.cache(filename=".train_cache")
        .shuffle(1000)
        .prefetch(buffer_size=AUTOTUNE)
    )
    val_ds = val_ds.cache(filename=".train_cache").prefetch(buffer_size=AUTOTUNE)

    model = tf.keras.models.Sequential(
        [
            layers.experimental.preprocessing.RandomFlip(
                "horizontal", input_shape=(img_height, img_width, 3)
            ),
            layers.experimental.preprocessing.RandomRotation(0.1),
            layers.experimental.preprocessing.RandomZoom(0.1),
            layers.experimental.preprocessing.Rescaling(1.0 / 255),
            layers.Conv2D(16, 3, padding="same", activation="relu"),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding="same", activation="relu"),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding="same", activation="relu"),
            layers.MaxPooling2D(),
            layers.Dropout(0.2),
            layers.Flatten(),
            layers.Dense(128, activation="relu"),
            layers.Dense(num_class),
        ]
    )

    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    history = model.fit(train_ds, validation_data=val_ds, epochs=nb_train)

    # loss, accuracy = model.evaluate(train_ds, train_lb)

    acc = history.history["accuracy"]
    val_acc = history.history["val_accuracy"]

    loss = history.history["loss"]
    val_loss = history.history["val_loss"]

    epochs_range = range(nb_train)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label="Training Accuracy")
    plt.plot(epochs_range, val_acc, label="Validation Accuracy")
    plt.legend(loc="lower right")
    plt.title("Training and Validation Accuracy")

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label="Training Loss")
    plt.plot(epochs_range, val_loss, label="Validation Loss")
    plt.legend(loc="upper right")
    plt.title("Training and Validation Loss")
    plt.show()

    model.save(settings["model_name"])


if __name__ == "__main__":
    train(sys.argv[1:])
