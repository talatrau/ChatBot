import re
import os
import numpy as np
import pickle
from underthesea import word_tokenize
from django.conf import settings


file = os.path.join(settings.BASE_DIR, 'chatbot\\model\\teencode.txt')
with open(file, 'r', encoding='UTF8') as f:
  teencodes = f.read().split('\n')

stopword = ['em', 'không', 'chị', 'này', 'shop', 'còn', 'ạ', 'mình']

file = os.path.join(settings.BASE_DIR, 'chatbot\\model\\intent_svm_tfidf')
with open(file, 'rb') as f:
  tf = pickle.load(f)

file = os.path.join(settings.BASE_DIR, 'chatbot\\model\\intent_svm')
with open(file, 'rb') as f:
  model = pickle.load(f)

label = {
  0: 'Changing',
  1: 'Connect',
  2: 'Done',
  3: 'Hello',
  4: 'Inform',
  5: 'Order',
  6: 'Other',
  7: 'Request',
  8: 'Return',
  9: 'feedback'
}



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

    pred = model.predict(clean_sentence)[0]

    return label[pred]

    
