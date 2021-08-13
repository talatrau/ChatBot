from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from chatbot.process import intent, getMessStack

# Create your views here.
@csrf_exempt
def answer(request):
    if request.method == 'POST':
        message = request.POST['message']
        intent(message)
        return JsonResponse({})
    elif request.method == 'GET':
        answer = getMessStack()
        return JsonResponse({'response': answer})