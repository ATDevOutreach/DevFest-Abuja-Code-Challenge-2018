from django.urls import path
from .views import home, signup, process_listen as SMSController, USSDController
    
urlpatterns = [
    path('', home, name='home'),
    path('listener/',  SMSController, name='listen'),
    path('ussd-listener/', USSDController.as_view(), name='ussd-listen'),
    path('signup/', signup, name='signup')
]