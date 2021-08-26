import os
import json
import time
from django.conf import settings
from chatbot.classification.text import Intent, Entity
from chatbot.classification.fashion import FashionImage
from chatbot.scenario import Scenario


### BEGIN GLOBAL VARIABLE ###

intent = Intent.getInstance()
entity = Entity.getInstance()
fashion = FashionImage.getInstance()
cache = {}

### END GLOBAL VARIABLE ###


def saveHistory(user, topic, text, isBot, img=None):
  """ save user chat history """

  img_src = ''

  if img:
    img_time = time.time()
    file_path = str(settings.BASE_DIR) + '\\media\\images\\' + user + "_" + str(img_time).replace('.', '') + ".jpg"
    img.save(file_path)
    img_src = 'http://localhost:8000/media/images/' + user + '_' + str(img_time).replace('.', '') + '.jpg'

  path = os.path.join(settings.BASE_DIR, 'chatbot\\chat_history')
  path = os.path.join(path, topic)

  if not os.path.exists(path):
    os.makedirs(path)

  json_path = path + '\\' + user + '_history.txt'
  jsonFile = open(json_path, "a")
  
  data = {'isbot': isBot, 'user': user, 'mess': text, 'src': img_src}
  jsonString = json.dumps(data) + "\n"
  jsonFile.write(jsonString)

  jsonFile.close()


def processMessage(user, topic, mess, file):
  """ process user message """

  global cache
  scienario = cache.get(user, Scenario())
  
  path = os.path.join(settings.BASE_DIR, 'chatbot\\chat_history')
  path = os.path.join(path, topic)

  if not os.path.exists(path):
    os.makedirs(path)

  fashion_id, img = fashion.getID(file)
  if fashion_id:
    scienario.setProductID(fashion_id)

  intent_class = intent.getClass(mess)
  entity_class = entity.getClass(mess)

  scienario.genResponse(intent_class, entity_class, mess)

  cache[user] = scienario
  saveHistory(user, topic, mess, False, img)


def getResponse(user = "talatrau", topic = "fashion"):
  global cache
  scienario = cache.get(user, Scenario())
  response = scienario.getResponse()
  cache[user] = scienario
  for mess in response:
    saveHistory(user, topic, mess, True)

  return response

