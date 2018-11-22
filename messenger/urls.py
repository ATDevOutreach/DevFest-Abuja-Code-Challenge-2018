from django.urls import path
from .views import process_listen, home, signup
from ussd.views import AfricasTalkingUssdGateway

urlpatterns = [
    path('', home, name='home'),
    path('listener/',  process_listen, name='listen'),
    path('ussd-listener/', AfricasTalkingUssdGateway.as_view(), name='ussd-listen'),
    path('signup/', signup, name='signup')
]