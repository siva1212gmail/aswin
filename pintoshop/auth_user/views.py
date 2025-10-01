# auth/views.py

from django.http import HttpResponse
from twilio.rest import Client

def home(request):
    return HttpResponse("Welcome to the Auth App")

# app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta,datetime

from .models import OTPVerification
from .serializer import SendOTPSerializer, VerifyOTPSerializer
from .utils import generate_otp, send_sms_via_twilio

class SendOTPView(APIView):
    def post(self, request):
        try:
            serializer = SendOTPSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            contact_value = serializer.validated_data['contact_value']

            otp_code = generate_otp()
            otp_obj = OTPVerification.objects.create(
                str_Contact_Value=contact_value,
                str_OTP_Code=otp_code,
                dte_Sent_Time=timezone.now()
            )

        # Assume if it's a phone number (basic check)
            if contact_value.startswith("+") and contact_value[1:].isdigit():
                send_sms_via_twilio(contact_value, otp_code)
                print("1")
            else:
                print("2")
            # Optional: email sending logic if needed
                pass

            return Response({"lng_OTP_ID": otp_obj.lng_OTP_ID}, status=status.HTTP_201_CREATED)
        except Exception as e:

            return Response(
                {"status": False, "message": f"Unable to send OTP {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

#
#
# class VerifyOTPView(APIView):
#     def post(self, request):
#         serializer = VerifyOTPSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         otp_id = serializer.validated_data['lng_OTP_ID']
#         input_otp = serializer.validated_data['otp_code']
#
#         try:
#             otp_obj = OTPVerification.objects.get(lng_OTP_ID=otp_id)
#         except OTPVerification.DoesNotExist:
#             return Response({"verified": False, "error": "Invalid OTP ID"}, status=404)
#
#         if otp_obj.str_OTP_Code != input_otp:
#             return Response({"verified": False, "error": "Invalid OTP"}, status=400)
#
#         if timezone.now() - otp_obj.dte_Sent_Time > timedelta(minutes=5):
#             return Response({"verified": False, "error": "OTP expired"}, status=400)
#
#         return Response({"verified": True})


class VerifyOTPView(APIView):
    def post(self, request):
        to_number = request.data.get('contact_value')
        otp_code = request.data.get('otp_code')
        account_sid = 'AC7eeefd0122473cc995d24ff86a5fe6a5'
        auth_token = "5b280d8c04ab681b63a7e4a3d4c61330"
        verify_sid = "VAcf0310873fc863a31683281836c49baf"  # e.g. VAcf0310...

        client = Client(account_sid, auth_token)

        try:
            verification_check = client.verify.services(verify_sid).verification_checks.create(
                to=to_number,
                code=otp_code
            )
            print(verification_check)
            print("Verification status:", verification_check.status)

            if verification_check.status == 'approved':
                return Response({"verified": True})
            else:
                return Response({"verified": False, "error": "Invalid OTP"}, status=400)
        except Exception as e:
            return Response({"verified": False, "error": str(e)}, status=500)
