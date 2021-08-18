from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from chatbot.process import intent, getMessStack

import io
import cv2
import numpy as np
from PIL import Image

# Create your views here.
@csrf_exempt
def answer(request):
    if request.method == 'POST':
        message = request.POST['message']
        chunks = request.FILES['img'].chunks()
        data = next(chunks)
        image = Image.open(io.BytesIO(data))
        image = np.array(image)
        img = cv2.resize(image, (100, 100))
        img = Image.fromarray(img, 'RGB')
        img.show()
        intent(message)
        return JsonResponse({})
    elif request.method == 'GET':
        answer = getMessStack()
        return JsonResponse({'response': answer})