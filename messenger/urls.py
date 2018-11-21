from django.urls import path
from .views import process_listen, home, signup

urlpatterns = [
    path('', home, name='home'),
    path('listener/',  process_listen, name='listen'),
    path('signup/', signup, name='signup')
]