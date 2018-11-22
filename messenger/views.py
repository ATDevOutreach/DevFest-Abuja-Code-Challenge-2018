from django.shortcuts import render
from .models import Hook
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
import re
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from ussd.core import UssdView, UssdRequest


# Homepage function
@login_required(login_url='/accounts/login/')
def home(request):
    return render(request, 'home.html', {})

# Function for User signuo
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Function that listens to SMS webhooks and send Email
@csrf_exempt
@require_POST
def process_listen(request):
    incoming_data = request.POST.copy()
    text_data = incoming_data.get('text')
    # Regex to search for email
    email = re.search(r'[\w\.-]+@[\w\.-]+', text_data)
    email = email.group(0)
    hook = Hook(data=text_data, type='SMS')
    hook.save()
    subject = 'Messenger'
    message = text_data
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail( subject, message, email_from, recipient_list )
    return HttpResponse("Email sent to {}".format(email))

# Function that listens to USSD Webhooks and send Email
class USSDController(UssdView):
    customer_journey_namespace = "USSDController"
    customer_journey_conf = settings.DEFAULT_USSD_SCREEN_JOURNEY
    
    def post(self, req):
        list_of_inputs = req.data['text'].split("*")
        text = "*" if len(list_of_inputs) >= 2 and list_of_inputs[-1] == "" and list_of_inputs[-2] == "" else list_of_inputs[
            -1]

        session_id = req.data['sessionId']
        if req.data.get('use_built_in_session_management', False):
            session_id = None
        ussd_request = UssdRequest(
            phone_number=req.data['phoneNumber'].strip('+'),
            session_id=session_id,
            ussd_input=text,
            service_code=req.data['serviceCode'],
            language=req.data.get('language', 'en'),
            use_built_in_session_management=req.data.get(
                'use_built_in_session_management', False)
        )
        text_data = "{}".format(req.data.get('text'))
        # Regex to search for email
        email = re.search(r'[\w\.-]+@[\w\.-]+', text_data)
        if (email):
            email = email.group(0)
            hook = Hook(data=text_data, type='USSD')
            hook.save()
            subject = 'Messenger'
            message = text_data
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail( subject, message, email_from, recipient_list )
        return ussd_request

    def ussd_response_handler(self, ussd_response):
        if self.request.data.get('serviceCode') == 'test':
            return super(USSDController, self).\
                ussd_response_handler(ussd_response)
        if ussd_response.status:
            res = 'CON' + ' ' + str(ussd_response)
            response = HttpResponse(res)
        else:
            res = 'END' + ' ' + str(ussd_response)
            response = HttpResponse(res)
        return response