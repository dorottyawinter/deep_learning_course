# -*- coding: utf-8 -*-
"""convolutional_neural_network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XTT1lzNgPSIzFgQ4R27R7VvXrXPGSMbG

# Convolutional Neural Network

### Importing the libraries
"""

import numpy as np
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image

tf.__version__

"""## Part 1 - Data Preprocessing

### Preprocessing the Training set
"""

train_datagen = ImageDataGenerator(rescale=1./255, # feature scaling: pixel values [0;1]
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

training_set = train_datagen.flow_from_directory('dataset/training_set',
                                                 target_size=(64, 64), # resize input pictures
                                                 batch_size=32,
                                                 class_mode='binary') # classification problem

"""### Preprocessing the Test set"""

# to avoid overfitting we will not apply any transformation on the test set, only rescaling

test_datagen = ImageDataGenerator(rescale=1./255)

test_set = test_datagen.flow_from_directory('dataset/validation_set',
                                            target_size=(64, 64),
                                            batch_size=32,
                                            class_mode='binary')

"""## Part 2 - Building the CNN

### Initialising the CNN
"""

cnn = tf.keras.models.Sequential()

"""### Step 1 - Convolution"""

cnn.add(
    tf.keras.layers.Conv2D(filters=32,
                           kernel_size=3,
                           activation='relu',
                           input_shape=(64,64,3)))

"""### Step 2 - Pooling"""

cnn.add(
    tf.keras.layers.MaxPool2D(pool_size=(2,2),
                              strides=2))

"""### Adding a second convolutional layer"""

cnn.add(
    tf.keras.layers.Conv2D(filters=32,
                           kernel_size=3,
                           activation='relu'))

cnn.add(
    tf.keras.layers.MaxPool2D(pool_size=(2,2),
                              strides=2))

"""### Step 3 - Flattening"""

cnn.add(tf.keras.layers.Flatten())

"""### Step 4 - Full Connection"""

cnn.add(
    tf.keras.layers.Dense(units=128,
                          activation='relu'))

"""### Step 5 - Output Layer"""

cnn.add(
    tf.keras.layers.Dense(units=1, # binary classification
                          activation='sigmoid')) # binary classification (multiclass classification: softmax activation)

"""## Part 3 - Training the CNN

### Compiling the CNN
"""

cnn.compile(optimizer='adam', loss='binary_cross_entropy', metrics='accuracy')

"""### Training the CNN on the Training set and evaluating it on the Test set"""

cnn.fit(x=training_set,
        validation_data=test_set, # no transformation was applied, only feature scaling
        epochs=25)

"""## Part 4 - Making a single prediction"""

test_image = image.load_image(path='dataset/single_prediction/cat_or_dog_1.jpg'
                              image_size=(64,64))
test_image = image.img_to_array(img=test_image) # convert to numpy array
test_image = np.expand_dims(a=test_image, axis=0) # extra dimension corresponding to the batch

result = cnn.predict(x=test_image)

training_set.class_indices # which indices corresponds to which classes # currently: 0 - cat, 1 - dog

if result[0][0] == 1: # result[<batch dimension>][<first prediction>]
  prediction = 'dog'
else:
  prediction = 'cat'

print(prediction)