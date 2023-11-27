import sys
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from keras.metrics import top_k_categorical_accuracy
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array

class LetterRecognition:

    def __init__(self, model_weights_path):
        self.model = self.load_model(model_weights_path)
        self.letters = 'ох'

    def load_model(self, model_weights_path):
        model = self.CNN_model()
        model.load_weights(model_weights_path)
        return model
    
    def top_3_categorical_accuracy(y_true, y_pred):
        return top_k_categorical_accuracy(y_true, y_pred, k=3)
    
    def CNN_model(self, activation='softmax', loss='categorical_crossentropy', optimizer='adam', metrics = ['accuracy', top_3_categorical_accuracy]):
        # Define image dimensions
        IMG_ROWS = 32
        IMG_COLS = 32
        # 3 stands for RGB images, 1 if greyscaled images
        INPUT_SHAPE = (IMG_ROWS, IMG_COLS, 3)
        # Number of classes to consider 
        NUM_CLASSES = 2
        letters = 'ох'

        model = Sequential()
        model.add(Conv2D(32, kernel_size = (3, 3),
                        activation = 'relu',
                        input_shape = INPUT_SHAPE))
        model.add(Conv2D(64, (3, 3), activation = 'relu'))
        model.add(Conv2D(128, (4, 4), activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation = 'relu'))
        model.add(Dropout(0.25))
        model.add(Dense(NUM_CLASSES, activation = activation))
    
        # Compile the model
        model.compile(loss = loss,
                    optimizer = optimizer, 
                    metrics = metrics)
        
        return model


    def load_image(self, path_filename):
        # load the image
        img = load_img(path_filename, target_size=(32, 32))
        # convert to array
        img = img_to_array(img)
        # reshape into a single sample with 1 channel
        img = img.reshape(1, 32, 32, 3)
        # prepare pixel data
        img = img.astype('float32')
        img = img / 255.0
        return img
    
    def recognize_letter(self, image_path):
        img = self.load_image(image_path)
        sys.stdout = open('nul','w')
        predicted_probs = self.model.predict(img)
        sys.stdout = sys.__stdout__
        a_letter = np.argmax(predicted_probs, axis=1)
        return self.letters[a_letter[0]]