from allauth.account.forms import SignupForm
from django import forms

from libs import AIRTIME, CARD, SMS
from libs.sms import SMS

from .fields import (CreditCardField, ExpiryDateField, PhoneField,
                     VerificationValueField)


class SignUpForm(SignupForm):
    phone_number = PhoneField(required=True)

    default_field_order = [
        'username',
        'email',
        'email2',  # ignored when not present
        'password1',
        'password2'  # ignored when not present
        'phone'
    ]

    def signup(self, request, user):
        """ Sign up and create new user """
        account = user.account.phone = self.cleaned_data['phone']
        account.save()


class SMSForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': '070xxxxxxxxxxx'}
        ),
        label='Phone',
    )
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'message'})
    )

    def clean_phone_number(self):
        telcoPrefixes = ['703', '706', '803', '806', '810', '813', '814', '816', '903', '705',
                         '805', '811', '815', '905', '701', '708', '802', '808', '812', '902',
                         '809', '817', '818', '909', '804']
        numbers = self.cleaned_data['phone_number'].split(',') if len(
            self.cleaned_data['phone_number']) > 1 else [self.cleaned_data['phone_number'], ]
        valid_numbers = []
        for number in numbers:
            if number[1:4] not in telcoPrefixes:
                raise forms.ValidationError(
                    f'{number} is not a valid Nigerian Phone number')
            valid_numbers.append(f'+234{number[1:]}')
        return valid_numbers

    def send_sms(self, sender):
        return SMS().send_sms_sync(
            self.cleaned_data['phone_number'],
            self.cleaned_data['message'],
            sender
        )


class PaymentForm(forms.Form):

    name_on_card = forms.CharField(max_length=50, required=True)
    card_number = CreditCardField(required=True)
    expiry_date = ExpiryDateField(required=True)
    cvv = VerificationValueField(required=True, label='CVV')
    pin = forms.IntegerField(
        required=True, max_value=9999,
        widget=forms.PasswordInput(
            attrs={'maxlength': 4, 'pattern': r"\d*"}),
        label='Pin')
    amount = forms.IntegerField(required=True)

    def make_payment(self):
        return CARD().checkout(
            self.cleaned_data['card_number'],
            self.cleaned_data['amount'],
            str(self.cleaned_data['pin']),
            self.cleaned_data['expiry_date'],
            int(self.cleaned_data['cvv']),

        )


class OTPForm(forms.Form):

    otp = forms.IntegerField(
        required=True, max_value=9999,
        widget=forms.PasswordInput(
            attrs={'maxlength': 4, 'pattern': r"\d*"}),
        label='OTP')

    def validate_payment(self, transaction_id):
        """ Validate Payment """
        return CARD().validate(
            transaction_id,
            self.cleaned_data['otp'],
        )


class RechargeAirtimeForm(forms.Form):
    phone_number = PhoneField(required=True)
    amount = forms.IntegerField(required=True)

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        return f"+234{phone[1:]}"

    def send_airtime(self):
        return AIRTIME().send_single(
            self.cleaned_data['phone_number'],
            str(self.cleaned_data['amount']))
