import africastalking
from django.conf import settings


def send(username: str, phone_number: str):
    africastalking.initialize(settings.AFRICAS_TALKING_USERNAME, settings.AFRICAS_TALKING_API_KEY)
    sms = africastalking.SMS
    response = sms.send(
        f"Hello {username}, your order has been received and it's being processed. Thank you for choosing us!",
        [phone_number],
        4187
    )
    return response
