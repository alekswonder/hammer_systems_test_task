from django.contrib.auth import get_user_model
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import AuthSerializer

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthSerializer

    @action(detail=False, methods=('post',))
    def auth(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        if serializer.validated_data.get('user_token'):
            request.user = Token.objects.get(
                key=serializer.validated_data.get('user_token')
            ).user
            return Response(serializer.validated_data, status.HTTP_200_OK)
        return Response(
            {'message': f'Было отправлено SMS-сообщение'
                        f' с кодом {serializer.data.get("otp_code")}'
             }, status.HTTP_200_OK
        )


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ...

