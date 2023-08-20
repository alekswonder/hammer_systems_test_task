from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (AuthSerializer, ReferralCodeSerializer,
                             UserProfileSerializer)
from user_profile.models import UserProfile

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthSerializer

    @action(detail=False, methods=('post',))
    def auth(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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


class UserProfileViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer

    @action(detail=False, methods=('get', 'post'))
    def me(self, request):
        user_profile = get_object_or_404(UserProfile, owner=request.user.id)
        serializer = self.get_serializer(user_profile)

        if not request.data.get('invite_code'):
            return Response(serializer.data, status.HTTP_200_OK)

        if user_profile.invite_code:
            return Response({'message': 'Вы не можете изменить пригласительный'
                                        ' код, который уже был введен'},
                            status.HTTP_405_METHOD_NOT_ALLOWED)

        invite_code = request.data.get('invite_code')
        user_profile.invite_code = invite_code
        data = {'invite_code': invite_code, 'host_user': request.user.pk}
        referral_serializer = ReferralCodeSerializer(data=data)

        if referral_serializer.is_valid(raise_exception=True):
            referral_serializer.save()
        else:
            return Response({'message': 'Невозможно создать связь между вами и'
                                        ' вашим рефералом'},
                            status.HTTP_400_BAD_REQUEST)

        user_profile.save()
        return Response(serializer.data, status.HTTP_200_OK)
