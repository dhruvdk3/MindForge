import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

# Define a simple CNN model with fewer convolutional layers, max pooling, and a fully connected neural network with sigmoid activation
def create_model():
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(155, 155, 1)))
    model.add(layers.MaxPooling2D((2, 2), strides=2))
    for _ in range(7):
        model.add(layers.Conv2D(32, (3, 3), activation='relu'))
        if _ % 2 == 0: # Apply max pooling after every alternate convolutional layer
            model.add(layers.MaxPooling2D((2, 2), strides=2))
    model.add(layers.Flatten())
    for _ in range(14):
        model.add(layers.Dense(128, activation='sigmoid'))
    model.add(layers.Dense(10, activation='softmax'))
    return model

# Load dataset (for example MNIST)
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

# Preprocess data using OpenCV
def preprocess_image(image):
    # Normalize pixel values
    normalized_image = image.astype('float32') / 255
    # Resize image to (155, 155)
    resized_image = cv2.resize(normalized_image, (155, 155))
    return resized_image

# Preprocess train and test images
train_images = np.array([preprocess_image(img) for img in train_images])
test_images = np.array([preprocess_image(img) for img in test_images])

# Add channel dimension
train_images = np.expand_dims(train_images, axis=-1)
test_images = np.expand_dims(test_images, axis=-1)

# Compile the model
model = create_model()
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(train_images, train_labels, epochs=5, batch_size=64)

# Evaluate the model
test_loss, test_acc = model.evaluate(test_images, test_labels)
print('Test accuracy:', test_acc)
