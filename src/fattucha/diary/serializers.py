from rest_framework import serializers

from diary.models import Products


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'name', 'brand', 'calories', 'protein', 'fat', 'carbohydrates', )
