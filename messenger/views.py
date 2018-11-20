from django.shortcuts import render
from .models import Hook
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


@csrf_exempt
def process_listen(request):
    incoming_data = request.POST.get('text')
    hook = Hook(data=incoming_data)
    hook.save
    return HttpResponse(incoming_data)