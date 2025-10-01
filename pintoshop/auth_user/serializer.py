# app/serializers.py
from rest_framework import serializers

class SendOTPSerializer(serializers.Serializer):
    contact_value = serializers.CharField(max_length=150)  # phone or email

class VerifyOTPSerializer(serializers.Serializer):
    lng_OTP_ID = serializers.IntegerField()
    otp_code = serializers.CharField(max_length=10)
