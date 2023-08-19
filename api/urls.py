from django.urls import path

from api.views import AuthAPIView, ProfileAPIView

app_name = 'api'

urlpatterns = [
    path('auth/', AuthAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view())
]
