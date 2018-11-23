from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from libs.sms import SMS

from .forms import OTPForm, PaymentForm, RechargeAirtimeForm, SMSForm
from .models import Activity, failed, pending, success


class IndexView(TemplateView):
    template_name = "index.html"


@method_decorator(login_required, name='dispatch')
class SendSMS(FormView):
    template_name = 'api/send_sms.html'
    form_class = SMSForm
    success_url = reverse_lazy('api:sms_success')
    failure_url = reverse_lazy('api:sms_failure')

    def form_valid(self, form):
        """ Checks if inputs are valid and sends the SMS """

        try:
            if not self.request.user.account.can_make_transaction(
                len(form.cleaned_data['phone_number']) * settings.COST_MESSAGE
            ):
                return redirect(reverse('api:low_balance'))
            res = form.send_sms('08176410891')
            if res['SMSMessageData']['Recipients'][0]['status'].lower() != 'success':
                raise Exception('Could not send')
            # print(json.load(res))
        except Exception as e:
            failed(self.request.user, 'SM', ','.join(
                form.cleaned_data['phone_number']))
            return redirect(self.failure_url)
        else:
            self.request.user.account.deduct(
                len(form.cleaned_data['phone_number']) * settings.COST_MESSAGE
            )
            success(self.request.user, 'SM', ','.join(
                form.cleaned_data['phone_number']))
            return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class SmsSuccessView(TemplateView):
    template_name = "api/sms_success.html"


@method_decorator(login_required, name='dispatch')
class SmsFailureView(TemplateView):
    template_name = 'api/sms_failure.html'


@method_decorator(login_required, name='dispatch')
class AirtimeRechargeView(FormView):
    form_class = RechargeAirtimeForm
    template_name = 'api/recharge_account.html'
    success_url = reverse_lazy('api:sms_success')
    failure_url = reverse_lazy('api:sms_failure')

    def form_valid(self, form):
        if not self.request.user.account.can_make_transaction(
            len(form.cleaned_data['phone_number']) * settings.COST_MESSAGE
        ):
            return redirect(reverse('api:low_balance'))
        res = None
        try:
            res = form.send_airtime()

        except Exception as e:
            raise Exception(e)
            failed(self.request.user, 'AR', ','.join(
                form.cleaned_data['phone_number']))
            return redirect(self.failure_url)
        else:
            print(res)
            success(self.request.user, 'AR', ','.join(
                form.cleaned_data['phone_number']))
            return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class RechargeAccountView(FormView):
    form_class = PaymentForm
    template_name = 'api/recharge_account.html'
    success_url = reverse_lazy('api:confirm_transaction')
    failure_url = reverse_lazy('api:sms_failure')

    def form_valid(self, form):
        res = None
        try:
            res = form.make_payment()
        except Exception as e:
            failed(self.request.user, 'RC')
            return redirect(self.failure_url)
        else:
            # If transaction has already being initialized
            if res['status'] == 'DuplicateRequest':
                return redirect('api:confirm_transaction')
            self.request.session['transaction_id'] = res['transactionId']
            self.request.session['recharge_amount'] = form.cleaned_data['amount']
            return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ConfirmTransacionView(FormView):
    form_class = OTPForm
    template_name = 'api/otp.html'
    success_url = reverse_lazy('api:sms_success')
    failure_url = reverse_lazy('api:sms_failure')

    def get(self, request, *args, **kwargs):
        """Handle GET requests: If a transaction has not being initialized
            redirect user to payment form
        """
        if request.session.get('transaction_id', None) is None:
            return redirect('api:recharge_account')
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        res = None
        try:
            res = form.validate_payment(self.request.session['transaction_id'])
            if res['status'] != 'Success':
                raise Exception('Failed')
        except Exception as e:
            failed(self.request.user, 'RC')
            return redirect(self.failure_url)
        else:
            success(self.request.user, 'RC',
                    self.request.session['recharge_amount'])
            self.request.user.account.recharge(
                self.request.session['recharge_amount'])
            self.request.session['checkout_token'] = res['checkoutToken']
            return super().form_valid(form)
        finally:
            del self.request.session['transaction_id']


@method_decorator(login_required, name='dispatch')
class HistoryView(TemplateView):
    template_name = 'api/history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = Activity.objects.filter(
            user=self.request.user).order_by('-date')
        return context
