from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import AuthSerializer


class AuthAPIView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data,
                                    context={'request': request})

        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({"message": "User registered successfully"},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "OTP generated, please verify"},
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
