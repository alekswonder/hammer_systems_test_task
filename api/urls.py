from django.urls import path

from api.views import AuthAPIView

app_name = 'api'

urlpatterns = [
    path('auth/', AuthAPIView.as_view()),
]
