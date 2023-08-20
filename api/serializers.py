from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from referral_code.models import ReferralCode
from user_profile.models import UserProfile
from utils.otp_generator import generate_otp
from utils.referral_code_generator import generate_referral_code
from utils.sms_service import send_sms
from utils.validators import validate_phone_number

User = get_user_model()


class AuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True,
                                         max_length=12,
                                         validators=(validate_phone_number, ))
    otp_code = serializers.CharField(required=False,
                                     max_length=4)

    def validate(self, attrs: dict) -> dict:
        phone_number: str = attrs.get('phone_number')
        otp_code: str = attrs.get('otp_code')

        if otp_code:
            stored_otp: str = self.get_stored_otp_from_cache(phone_number)
            if stored_otp and otp_code == stored_otp:
                try:
                    user = User.objects.get(username=phone_number)
                except User.DoesNotExist:
                    user = User.objects.create(username=phone_number)
                    profile = UserProfile.objects.create(
                        owner=user,
                        phone_number=phone_number,
                        referral_code=generate_referral_code(),
                    )
                    user.save()
                    profile.save()
                token, created = Token.objects.get_or_create(user=user)
                attrs['user_token'] = str(token.key)
            else:
                raise serializers.ValidationError('Неверный SMS-код')
        else:
            otp_code = generate_otp()
            send_sms(phone_number, otp_code)
            attrs['otp_code'] = otp_code
            self.store_otp_in_cache(phone_number, otp_code)
        return attrs

    def store_otp_in_cache(self, phone_number: str,
                           otp_code: str) -> None:
        cache_key = 'otp_codes'
        otp_codes = cache.get(cache_key, {})
        otp_codes[phone_number] = otp_code
        cache.set(cache_key, otp_codes, timeout=300)

    def get_stored_otp_from_cache(self, phone_number: str) -> str:
        cache_key = 'otp_codes'
        otp_codes = cache.get(cache_key, {})
        return otp_codes.get(phone_number, None)


class ReferralCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferralCode
        fields = ('invite_code', 'host_user', )


class UserProfileSerializer(serializers.ModelSerializer):
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('phone_number', 'referral_code', 'invite_code', 'referrals')

    def get_referrals(self, obj) -> tuple:
        referrals = ReferralCode.objects.filter(
            invite_code=obj.referral_code
        ).select_related('host_user').all()
        return tuple(ref.host_user.profile.phone_number for ref in referrals)
