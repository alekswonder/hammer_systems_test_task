from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import serializers

from utils.invite_code_generator import generate_invite_code
from utils.otp_generator import generate_otp
from utils.sms_service import send_sms
from utils.validators import validate_phone_number

User = get_user_model()


class AuthSerializer(serializers.ModelSerializer):
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
        otp_code = None

        if 'otp_code' not in validated_data:
            otp_code = generate_otp()
            send_sms(otp_code)
            self.store_otp_in_cache(phone_number, otp_code)
            return {}

        stored_opt = self.get_stored_otp_from_cache(phone_number)
        if stored_opt and validated_data['otp_code'] == stored_opt:
            user = User.objects.create_user(username=phone_number,
                                            phone_number=phone_number,
                                            invite_code=generate_invite_code())
            return user
        else:
            raise serializers.ValidationError('Неверный временный пароль')

    def store_otp_in_cache(self, phone_nuber: str, otp_code: str) -> None:
        cache_key = 'otp_codes'
        otp_codes = cache.get(cache_key, {})
        otp_codes[phone_nuber] = otp_code
        cache.set(cache_key, otp_codes, timeout=300)

    def get_stored_otp_from_cache(self, phone_nuber: str) -> int:
        cache_key = 'otp_codes'
        otp_codes = cache.get(cache_key, {})
        return otp_codes.get(phone_nuber, None)
