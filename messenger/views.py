from django.shortcuts import render
from .models import Hook
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import re

@csrf_exempt
@require_POST
def process_listen(request):
    incoming_data = request.POST.copy()
    text_data = incoming_data.get('text')
    # Regex to search for email
    email = re.search(r'[\w\.-]+@[\w\.-]+', text_data)
    email = email.group(0)
    hook = Hook(data=text_data)
    hook.save()
    subject = 'Messenger'
    message = text_data
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail( subject, message, email_from, recipient_list )
    print(email)
    return HttpResponse("Email sent to {}".format(email))