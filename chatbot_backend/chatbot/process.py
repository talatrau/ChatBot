import re
import os
import json
import time
import numpy as np
import pickle
import io
import cv2
import tensorflow
from PIL import Image
from underthesea import word_tokenize
from django.conf import settings
from tensorflow.keras import layers, Model
from chatbot.models import Company, Fashion


### BEGIN LOAD INTENT CLASSIFICATION MODEL ###
file = os.path.join(settings.BASE_DIR, 'chatbot\\model\\teencode.txt')
with open(file, 'r', encoding='UTF8') as f:
  teencodes = f.read().split('\n')

stopword = ['em', 'không', 'chị', 'này', 'shop', 'còn', 'ạ', 'mình']

file = os.path.join(settings.BASE_DIR, 'chatbot\\model\\intent_svm_tfidf')
with open(file, 'rb') as f:
  tf = pickle.load(f)

file = os.path.join(settings.BASE_DIR, 'chatbot\\model\\intent_svm')
with open(file, 'rb') as f:
  intent_model = pickle.load(f)
### END LOAD INTENT CLASSFICATION MODEL ###

### BEGIN LOAD IMAGE CLASSIFICATION MODEL ###
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
### END LOAD IMAGE CLASSIFICATION MODEL ###

mess_stack = []

def __label2Intent(label):
  if label == 0:
    return 'Changing'
  elif label == 1:
    return 'Connect'
  elif label == 2:
    return 'Done'
  elif label == 3:
    return 'Hello'
  elif label == 4:
    return 'Inform'
  elif label == 5:
    return 'Order'
  elif label == 6:
    return 'Other'
  elif label == 7:
    return 'Request'
  elif label == 8:
    return 'Return'
  elif label == 9:
    return 'feedback'


def __label2Fashion(label):
  if label == 0:
    return 'D001'
  elif label == 1:
    return 'D0011'
  elif label == 2:
    return 'D0012'
  elif label == 3:
    return 'D0013'
  elif label == 4:
    return 'D0014'
  elif label == 5:
    return 'D0015'
  elif label == 6:
    return 'D0016,17'
  elif label == 7:
    return 'D003'
  elif label == 8:
    return 'D004'
  elif label == 9:
    return 'D005'
  elif label == 10:
    return 'D006,7'
  elif label == 11:
    return 'D008'
  elif label == 12:
    return 'D009'
  elif label == 13:
    return 'DS001'
  elif label == 14:
    return 'S002'
  elif label == 15:
    return 'S003'
  elif label == 16:
    return 'S004'
  elif label == 17:
    return 'S005'
  elif label == 18:
    return 'S006'
  elif label == 19:
    return 'S008'
  elif label == 20:
    return 'S009'


def datapreprocessing(data, stop_words):
  for i in range(len(data)):
    data[i] = re.sub(r'Khách \d+', '', data[i]).lower()

  texts = ' \t '.join(text for text in data)
  texts = re.sub(r'[!@?:.,;%<>()\'*\+\-&$#/_|"]+|xx+', ' ', texts)
  
  for teencode in teencodes:
    teencode = teencode.split('\t')
    texts = re.sub(r'\b{}\b'.format(teencode[0]), teencode[1], texts)

  for word in stop_words:
    texts = re.sub(r'\b{}\b'.format(word), ' ', texts)

  X = texts.split(' \t ')
  X = np.array(X)

  return [word_tokenize(str(x), format='text') for x in X]


def intent(sentence):
  clean_sentence = datapreprocessing([sentence], stopword)
  clean_sentence = tf.transform(clean_sentence).toarray()

  pred = intent_model.predict(clean_sentence)[0]

  return __label2Intent(pred)


def fashionImg(rawData):
  image = Image.open(io.BytesIO(rawData))
  img = np.array(image)
  img = cv2.resize(img, (224, 224))
  img = img.reshape(1, 224, 224, 3)
  X_input = img / 255
  prediction = np.argmax(fashion_model.predict(X_input))
  q = Fashion.objects.get(pk=__label2Fashion(prediction)).__dict__
  res = "ID: {} | {} - {} - size {} - {}".format(q['id'], q['name'], q['color'], q['size'], q['brand_id'])

  return res, image



def processMessage(user, topic, mess, file):
  text = mess
  img_src = ""
  intent_mess = ""
  fashion_mess = ""

  path = os.path.join(settings.BASE_DIR, 'chatbot\\chat_history')
  path = os.path.join(path, topic)

  if not os.path.exists(path):
    os.makedirs(path)

  if mess:
    intent_mess = intent(mess)
    mess_stack.append({'isbot': True, 'user': user, 'mess': intent_mess, 'src': ""})
  
  if file: 
    fashion_mess, img = fashionImg(file)
    file_path = str(settings.BASE_DIR) + '\\media\\images\\' + user + "_" + str(time.time()).replace('.', '') + ".jpg"
    img_src = 'http://localhost:8000/media/images/' + user + '_' + str(time.time()).replace('.', '') + '.jpg'
    img.save(file_path)
    mess_stack.append({'isbot': True, 'user': user, 'mess': fashion_mess, 'src': ""})

  json_path = path + '\\' + user + '_history.txt'
  jsonFile = open(json_path, "a")
  
  data = {'isbot': False, 'user': user, 'mess': text, 'src': img_src}
  jsonString = json.dumps(data) + "\n"
  jsonFile.write(jsonString)

  if intent_mess:
    data = {'isbot': True, 'user': user, 'mess': intent_mess, 'src': ""}
    jsonString = json.dumps(data) + "\n"
    jsonFile.write(jsonString)

  if fashion_mess:
    data = {'isbot': True, 'user': user, 'mess': fashion_mess, 'src': ""}
    jsonString = json.dumps(data) + "\n"
    jsonFile.write(jsonString)

  jsonFile.close()


def getMessStack():
  global mess_stack
  res = mess_stack
  mess_stack = []
  return res

    
