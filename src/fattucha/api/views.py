from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from diary.models import Products
from diary.serializers import ProductSerializer


class ProductModalViewSet(ModelViewSet):
    queryset = Products.objects.all().order_by('id')
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('get',):
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()
