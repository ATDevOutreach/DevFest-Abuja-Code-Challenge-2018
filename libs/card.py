import africastalking
from django.conf import settings


class CARD:
    def __init__(self):
        # Set your app credentials
        self.username = settings.AT_USERNAME
        self.api_key = settings.AT_API_KEY
        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)
        # Get the payments service
        self.payment = africastalking.Payment

    def checkout(self, number, amount, auth_token, expiry_date,
                    cvv, country_code='NG', checkout_token=None):
        # Set the name of your Africa's Talking payment product
        productName = settings.AT_PRODUCT_NAME
        # Set the details of the payment card to be charged
        card = {
            'number': number,
            'countryCode': country_code,
            'cvvNumber': cvv,
            'expiryMonth': expiry_date.month,
            'expiryYear': expiry_date.year,
            'authToken': auth_token
        }
        # If you already have a valid checkout token for the card user, as a result of a
        # previous successful validation,
        # you can charge the card by passing in the checkout token instead of sending
        # the full card information again.
        checkout_token = None
        # Set The 3-Letter ISO currency code and the checkout amount
        currencyCode = "NGN"
        amount = amount
        # Set a description of the transaction to be displayed on the clients statement
        narration = 'Subscription for xms'
        # Set any metadata that you would like to send along with this request.
        # This metadata will be included when we send back the final payment notification
        metadata = {
            'requestId': "1234",
            'applicationId': "abcde"
        }
        return  self.payment.card_checkout(
                productName, currencyCode, amount, narration, card, checkout_token, metadata)

    def validate(self, transaction_id, otp):
        """ Validate card Transaction """
        # Set the transactionId you got from the card checkout charge request
        transaction_id = transaction_id
        # Set the OTP given to you by the user you're charging
        otp = otp
        # That's it, hit send and we'll take care of the rest
        return self.payment.validate_card_checkout(transaction_id, otp)
