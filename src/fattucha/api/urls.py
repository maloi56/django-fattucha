from django.urls import path, include

from rest_framework import routers
from api.views import ProductModalViewSet

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'products', ProductModalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
