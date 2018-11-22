""" A library for sending SMS """
import africastalking
from django.conf import settings


class SMS:
    def __init__(self):
        # Set your app credentials
        self.username = settings.AT_USERNAME
        self.api_key = settings.AT_API_KEY
        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)
        # Get the SMS service
        self.sms = africastalking.SMS

    def send_sms_sync(self, recipients, message, sender=False):
        return self.sms.send(message, recipients)
