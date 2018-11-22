from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from libs.sms import SMS

from .forms import SMSForm


class IndexView(TemplateView):
	template_name = "index.html"


class SendSMS(FormView):
	template_name = 'api/send_sms.html'
	form_class = SMSForm
	success_url = reverse('api:sms_success')
	failure_url = reverse('api:sms_failure')

	def form_valid(self, form):
		""" Checks if inputs are valid and sends the SMS """

		try:
			form.send_sms()
		except Exception as e:
			return redirect(self.failure_url)
		else:
			return super().form_valid(form)


class SmsSuccessView(TemplateView):
	template_name = "api/sms_success.html"


class SmsFailureView(TemplateView):
	template_name = 'api/sms_failure.html'
