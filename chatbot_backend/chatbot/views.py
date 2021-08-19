from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from chatbot.process import intent, getMessStack, fashionImg

# Create your views here.
@csrf_exempt
def answer(request):
    if request.method == 'POST':
        if request.POST['message']:    
            message = request.POST['message']
            intent(message)

        if request.FILES['img']:
            chunks = request.FILES['img'].chunks()
            data = next(chunks)
            fashionImg(data)
            
        return JsonResponse({})
    elif request.method == 'GET':
        answer = getMessStack()
        return JsonResponse({'response': answer})