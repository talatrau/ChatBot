import os
import io
import cv2
import tensorflow
import numpy as np
from PIL import Image
from tensorflow.keras import layers, Model
from django.conf import settings


class FashionImage:
    __instance = None
    TARGET_NAME = ['D001', 'D0011', 'D0012', 'D0013', 'D0014', 'D0015', 'D0016,17', 'D003', 'D004', 'D005', 
                    'D006,7', 'D008', 'D009', 'DS001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S008', 'S009']


    @staticmethod
    def getInstance():
        if FashionImage.__instance == None:
            FashionImage()
        return FashionImage.__instance


    def __init__(self):
        if FashionImage.__instance != None:
            raise Exception("This is a singleton")
        else:
            super().__init__()

            fashion_model = tensorflow.keras.applications.MobileNetV2()
            last_layer = fashion_model.get_layer("global_average_pooling2d")
            x = layers.Dense(1280, activation='relu')(last_layer.output)
            x = layers.Dropout(0.1)(x)
            x = layers.Dense(1280, activation='relu')(x)
            x = layers.Dropout(0.1)(x)
            x = layers.Dense(21, activation='softmax')(x)
            fashion_model = Model(fashion_model.input, x)
            file = os.path.join(settings.BASE_DIR, 'chatbot\\model\\fashion_weight.h5')
            fashion_model.load_weights(file)

            self.model = fashion_model

            FashionImage.__instance = self


    def __label2class(self, label):
        return self.TARGET_NAME[label]

    
    def getID(self, rawData):
        if rawData:
            image = Image.open(io.BytesIO(rawData))
            img = np.array(image)
            img = cv2.resize(img, (224, 224))
            img = img.reshape(1, 224, 224, 3)
            X_input = img / 255
            label = np.argmax(self.model.predict(X_input))
            
            return self.__label2class(label), image
        else:
            return None, None