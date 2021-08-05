from rest_framework import serializers

from product.models import Product, SubProduct, Type, Unit


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = ['id',  'name', 'description']


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = ['id',  'name', 'description', 'abr']


class SubProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubProduct
        fields = ['id', 'product', 'stock', 'real', 'description',
                  'unit_price', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):

    type_detail = TypeSerializer(source='type', read_only=True)
    unit_detail = UnitSerializer(source='unit', read_only=True)
    sub_product = SubProductSerializer(many=True, read_only=True)

    # def update(self, instance, validated_data):
    #     instance.type = validated_data.get('type', instance.type)
    #     instance.unit = validated_data.get('unit', instance.unit)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.unit_price = validated_data.get('unit_price', instance.unit_price)

    #     stock = validated_data.get('stock', instance.stock)
    #     instance.stock = instance.stock + stock
    #     instance.save()
    #     return instance

    class Meta:
        model = Product
        fields = [
            # Create or Update Fields
            'id',
            'type',
            'unit',
            'code',
            'name',
            'description',

            # Read only Fields
            'created_at',
            'updated_at',

            # Attribute Fields
            'total_stock',
            'current_price',

            # Nested Fields
            'sub_product',
            'type_detail',
            'unit_detail'
        ]
