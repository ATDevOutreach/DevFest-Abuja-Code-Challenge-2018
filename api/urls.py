from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('sms/', views.SendSMS.as_view(), name='send_sms'),
    path('sms/success', views.SmsSuccessView.as_view(), name='sms_success'),
    path('sms/failure', views.SmsFailureView.as_view(), name='sms_failure'),

]
