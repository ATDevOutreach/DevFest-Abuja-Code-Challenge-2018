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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['sms_sent'] = Activity.sms_sent(self.request.user.username)
            context['airtime_recharged'] = Activity.airtime_recharged(self.request.user.username)
        return context

@method_decorator(login_required, name='dispatch')
class SendSMS(FormView):
    template_name = 'api/send_sms.html'
    form_class = SMSForm
    success_url = reverse_lazy('api:send_sms')

    def form_valid(self, form):
        """ Checks if inputs are valid and sends the SMS """

        try:
            if not self.request.user.account.can_make_transaction(
                len(form.cleaned_data['phone_number']) * settings.COST_MESSAGE
            ):
                failed(self.request, 'AR', "Insufficient Balance",
                message="Insufficient Balance"
            )
                return redirect(reverse('api:index'))
            res = form.send_sms('08176410891')
            if res['SMSMessageData']['Recipients'][0]['status'].lower() != 'success':
                raise Exception('Could not send')
            # print(json.load(res))
        except Exception as e:
            failed(
                self.request, 'SM', ','.join(
                    form.cleaned_data['phone_number']),
                message="There was a problem sending your sms, Try again later"
            )
        else:
            self.request.user.account.deduct(
                len(form.cleaned_data['phone_number']) * settings.COST_MESSAGE)
            success(
                self.request, 'SM', ','.join(form.cleaned_data['phone_number']),
                message=(f"Your SMS to {form.cleaned_data['phone_number']} was sent"
                         "successfully"
                         ))
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class AirtimeRechargeView(FormView):
    form_class = RechargeAirtimeForm
    template_name = 'api/airtime_recharge.html'
    success_url = reverse_lazy('api:airtime_recharge')

    def form_valid(self, form):
        if not self.request.user.account.can_make_transaction(
            form.cleaned_data['amount']
        ):
            failed(self.request, 'AR', "Insufficient Balance",
                message="Insufficient Balance"
            )
            return redirect(reverse('api:index'))
        res = None
        try:
            res = form.send_airtime()

        except Exception as e:
            failed(self.request, 'AR', form.cleaned_data['phone_number'],
                message="Could not complete Airtime Recharge, try again later"
            )
        else:
            success(self.request, 'AR', form.cleaned_data['phone_number'],
            message=f"Your recharge of N{form.cleaned_data['amount']} was successful"
            )
            self.request.user.account.deduct(form.cleaned_data['amount'])
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
            failed(self.request, 'RC', message="Could not complete Transaction. Try again later")
        else:
            # If transaction has already being initialized
            pending(self.request, 'RC', message=("an OTP was sent to your registered number, "
            "enter it to continue"))
            if res['status'] == 'DuplicateRequest':
                return redirect('api:confirm_transaction')
            self.request.session['transaction_id'] = res['transactionId']
            self.request.session['recharge_amount'] = form.cleaned_data['amount']
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ConfirmTransacionView(FormView):
    form_class = OTPForm
    template_name = 'api/otp.html'
    success_url = reverse_lazy('api:index')

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
            failed(self.request, 'RC', self.request.session['recharge_amount'],
            message="Transaction Failed. Try again later")
        else:
            success(self.request, 'RC', self.request.session['recharge_amount'],
                "Transaction Successful"
            )
            self.request.user.account.recharge(
                self.request.session['recharge_amount'])
            self.request.session['checkout_token'] = res['checkoutToken']
        del self.request.session['transaction_id']
        del self.request.session['recharge_amount']
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class HistoryView(TemplateView):
    template_name = 'api/history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = Activity.objects.filter(
            user=self.request.user).order_by('-date')
        return context
