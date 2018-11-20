from django.urls import path
from .views import process_listen

urlpatterns = [
    path('listener/',  process_listen)
]