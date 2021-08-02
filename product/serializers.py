from rest_framework import serializers

from product.models import Product, Type, Unit


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = ['id',  'name', 'description']


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = ['id',  'name', 'description', 'abr']


class ProductSerializer(serializers.ModelSerializer):

    type_detail = TypeSerializer(source='type', read_only=True)
    unit_detail = UnitSerializer(source='unit', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'type', 'unit', 'code', 'name', 'description', 'unit_price', 'stock', 'type_detail', 'unit_detail']
