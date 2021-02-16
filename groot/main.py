import tensorflow as tf
from tensorflow import keras
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import sys
# import redis


def main(argv):
    # database = redis.Redis(host='localhost', port=6379, db=0)
    model_name = argv[0]

    img_path = argv[1]
    img_height = int(argv[2])
    img_width = int(argv[3])

    class_names = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']

    model = keras.models.load_model(model_name)

    # par url : 
    # sunflower_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg"
    # par path :

    img = keras.preprocessing.image.load_img(
        img_path, target_size=(img_height, img_width)
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
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
    main(sys.argv[1:])
