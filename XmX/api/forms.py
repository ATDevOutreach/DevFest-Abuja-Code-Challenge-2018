from django import forms

from libs.sms import SMS


class SMSForm(forms.Form):
    phone_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'placeholder': 'Phone Number'}
        ),
        label='Phone'
    )
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'message'})
    )

    def send_sms(self):
        SMS().send_sms_sync(
            (self.cleaned_data['phone_number'], ), self.cleaned_data['message'])
