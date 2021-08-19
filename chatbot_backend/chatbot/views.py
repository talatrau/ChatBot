from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from chatbot.process import getMessStack, processMessage

# Create your views here.
@csrf_exempt
def answer(request):
    if request.method == 'POST':
        message = ""
        data = None
        user = request.POST['user']
        topic = request.POST['topic']

        if request.POST['message']:    
            message = request.POST['message']

        try:
            chunks = request.FILES['img'].chunks()
            data = next(chunks)
        except:
            pass

        processMessage(user, topic, message, data)

        return JsonResponse({})
    elif request.method == 'GET':
        answer = getMessStack()
        return JsonResponse({'response': answer})


def getImage(request, img):
    if request.method == 'GET':
        src = "/media/images/" + img
        html = """ 
                <img src={} alt="image" />
            """.format(src)

        return HttpResponse(html)