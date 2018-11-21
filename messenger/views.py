from django.shortcuts import render
from .models import Hook
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

@csrf_exempt
def process_listen(request):
    incoming_data = json.loads(request.body)
    text_data = "{}".format(incoming_data['text'])
    hook = Hook(data=text_data)
    hook.save()
    print(text_data)
    return HttpResponse(text_data)