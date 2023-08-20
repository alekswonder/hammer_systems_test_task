from django.urls import path

from api.views import AuthViewSet, UserProfileViewSet

app_name = 'api'


urlpatterns = [
    path('auth/', AuthViewSet.as_view({'post': 'auth'}), name='auth'),
    path('profile/me/',
         UserProfileViewSet.as_view({'get': 'me', 'post': 'me'}),
         name='profile-me'),
]

