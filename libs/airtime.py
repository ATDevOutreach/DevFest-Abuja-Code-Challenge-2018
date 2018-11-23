import africastalking
from django.conf import settings


class AIRTIME:
    def __init__(self):
        # Set your app credentials
        self.username = settings.AT_USERNAME
        self.api_key = settings.AT_API_KEY
        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)
        # Get the airtime service
        self.airtime = africastalking.Airtime

    def send_single(self, phone_number, amount, currency_code='NGN'):
        return self.airtime.send(
            phone_number=phone_number, amount=amount, currency_code=currency_code)
