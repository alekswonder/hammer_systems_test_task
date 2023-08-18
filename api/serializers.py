from django.contrib.auth import get_user_model
from rest_framework import serializers

from utils.validators import validate_phone_number

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    otp_code = serializers.CharField(write_only=True, max_length=6,
                                     allow_blank=True)

    class Meta:
        model = User
        fields = ('phone_number', 'otp_code', )
        extra_kwargs = {
            'phone_number': {'validators': (validate_phone_number, )}
        }
