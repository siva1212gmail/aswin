# app/utils.py
import random
from twilio.rest import Client
from rest_framework.response import Response
from django.conf import settings

def generate_otp():
    return str(random.randint(1000, 9999))

def send_sms_via_twilio(to_number, otp_code):
    account_sid = 'AC7eeefd0122473cc995d24ff86a5fe6a5'
    auth_token = "5b280d8c04ab681b63a7e4a3d4c61330"
    verify_sid = "VAcf0310873fc863a31683281836c49baf"  # e.g. VAcf0310...

    client = Client(account_sid, auth_token)

    try:
        verification = client.verify.services(verify_sid).verifications.create(
            to='+916383560813',
            channel='sms'
        )
        print(f"Verification status: {verification.status}")
    except Exception as e:
        print(e)
        return Response({"message":e})

    return verification.status
