from builtins import quit

from rest_framework import serializers

from client.serializers import ClientSerializer
from product.serializers import ProductSerializer
from service.models import Service, ServiceProductDetail


# Serializers para los servicios


class ServiceProductSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)

    def create(self, validated_data):
        quantity = self.validated_data['quantity']
        product = self.validated_data['product']
        product.stock -= quantity
        product.save()
        return ServiceProductDetail.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.service = validated_data.get('service', instance.service)
        instance.description = validated_data.get('description', instance.description)

        """
        If:
            1. Validar si son el mismo producto
            2. Actualiza el valor del stock del product segun la cantidad
        Else:
            1. Validar si no son el mismo producto
            2. Actualiza el valor del stock del product actual
            2. Actualiza el valor del stock del nuevo product
        """
        if instance.product == validated_data['product']:
            product = instance.product
            quantity = instance.quantity - validated_data['quantity']
            product.stock += quantity
            product.save()
        else:
            current_product = instance.product
            current_product.stock += instance.quantity
            current_product.save()

            new_product = validated_data['product']
            quantity = validated_data['quantity']
            new_product.stock -= quantity
            new_product.save()

        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.product = validated_data.get('product', instance.product)
        instance.save()
        return instance

    class Meta:
        model = ServiceProductDetail
        fields = ['id', 'service', 'product', 'product_detail', 'description', 'quantity', 'total']


class ServiceSerializer(serializers.ModelSerializer):
    # service_products = ServiceProductSerializer(many=True, read_only=True)
    service_products = serializers.SerializerMethodField()
    client_detail = ClientSerializer(source='client', read_only=True)

    class Meta:
        model = Service
        fields = [
            'id',
            'client',
            'client_detail',
            'code',
            'estimated_price',
            'final_price',
            'init_date',
            'end_date',
            'observations',
            'name',
            'state',
            'service_products',
        ]

    def get_service_products(self, instance):
        data = instance.service_products.all().order_by('-id')
        return ServiceProductSerializer(data, many=True, read_only=True).data
