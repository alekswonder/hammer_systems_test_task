from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import AuthViewSet

app_name = 'api'

router_api_v1 = DefaultRouter()

router_api_v1.register(
    r'',
    AuthViewSet,
    basename=''
)

urlpatterns = [
    path('v1/', include(router_api_v1.urls))
]
