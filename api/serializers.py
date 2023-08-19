from django.contrib.auth import get_user_model
from rest_framework import serializers

from referral_code.models import ReferralCode
from utils.referral_code_generator import generate_referral_code
from utils.validators import validate_phone_number

User = get_user_model()


class AuthWithOTPSerializer(serializers.ModelSerializer):
    otp_code = serializers.CharField(write_only=True, max_length=4,
                                     required=False)

    class Meta:
        model = User
        fields = ('phone_number', 'otp_code',)
        extra_kwargs = {
            'phone_number': {'validators': (validate_phone_number,)}
        }

    def create(self, validated_data: dict):
        phone_number = validated_data['phone_number']
        otp_code = validated_data['otp_code']
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            user = User.objects.create_user(
                phone_number=phone_number,
                referral_code=generate_referral_code())
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'invite_code', 'referral_code', 'referrals')

    def get_referrals(self, obj):
        referrals = ReferralCode.objects.select_related('host_name')
        return []

    def validate(self, attrs):
        ...
