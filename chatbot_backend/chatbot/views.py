from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from chatbot.process import intent

# Create your views here.
@csrf_exempt
def answer(request):
    if request.method == 'POST':
        message = request.POST['message']
        answer = intent(message)
        return JsonResponse({'answer': answer})
    elif request.method == 'GET':
        return HttpResponse("hello world")