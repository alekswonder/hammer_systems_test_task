from rest_framework.views import APIView

from api.serializers import LoginSerializer


class SignUpView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp_code = serializer.validated_data['otp_code']

            try:
                ...
            except Exception:
                ...
