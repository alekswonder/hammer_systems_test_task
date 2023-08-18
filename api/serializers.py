from django.contrib.auth import get_user_model
from rest_framework import serializers

from utils.invite_code_generator import generate_invite_code
from utils.validators import validate_phone_number

User = get_user_model()


class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone_number', )
        extra_kwargs = {
            'phone_number': {'validators': (validate_phone_number,)}
        }


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
            user = User.objects.get(username=phone_number)
        except User.DoesNotExist:
            user = User.objects.create_user(username=phone_number,
                                            invite_code=generate_invite_code())
        return user
