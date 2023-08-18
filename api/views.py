from django.contrib.auth import login, logout
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import AuthSerializer, AuthWithOTPSerializer
from utils.otp_generator import generate_otp
from utils.sms_service import send_sms


class AuthAPIView(APIView):
    def get(self, request):
        return Response({'username': request.user.username})

    @csrf_exempt
    def post(self, request):
        phone_number: str = request.data.get('phone_number')
        otp_code: str = request.data.get('otp_code')

        if otp_code:
            stored_otp = self.get_stored_otp_from_cache(phone_number)
            if stored_otp and otp_code == stored_otp:
                serializer = AuthWithOTPSerializer(
                    data=request.data,
                    context={'request': request}
                )
                if serializer.is_valid():
                    user = serializer.save()
                    if user:
                        login(request, user)
                        return Response({'message': 'User authorized'},
                                        status=status.HTTP_200_OK)
                    else:
                        return Response({'message': 'Authentication failed'},
                                        status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({'message': 'Something went wrong'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': 'Invalid OTP code'},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            otp_code = generate_otp()
            send_sms(otp_code)
            self.store_otp_in_cache(request.data.get('phone_number'), otp_code)
            return Response({"message": "OTP sent successfully"},
                            status=status.HTTP_200_OK)

    def clear_cookies(self, request):
        logout(request)
        request.session.flush()

    def store_otp_in_cache(self, phone_number: str, otp_code: str) -> None:
        cache_key = 'otp_codes'
        otp_codes = cache.get(cache_key, {})
        otp_codes[phone_number] = otp_code
        cache.set(cache_key, otp_codes, timeout=300)

    def get_stored_otp_from_cache(self, phone_number: str) -> int:
        cache_key = 'otp_codes'
        otp_codes = cache.get(cache_key, {})
        return otp_codes.get(phone_number, None)
