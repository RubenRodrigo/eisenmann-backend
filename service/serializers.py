from rest_framework import serializers

from client.serializers import ClientSerializer
from product.serializers import ProductSerializer, ProductStockSerializer
from service.models import Service, ServiceProductDetail
from employee.serializers import EmployeeSerializer


# Serializers para los servicios


class ServiceProductSerializer(serializers.ModelSerializer):
    product_detail = ProductStockSerializer(source='product', read_only=True)
    employee_detail = EmployeeSerializer(source='employee', read_only=True)

    def validate(self, data):
        print(data)
        if data['quantity'] > data['product'].total_stock:
            raise serializers.ValidationError("no_stock")
        return data

    def create(self, validated_data):
        quantity = validated_data['quantity']
        product = validated_data['product']
        product_entries = product.product_entry.all().order_by('created_at')

        new_stock = quantity

        for product_entry in product_entries:
            new_stock = new_stock - product_entry.stock
            if new_stock > 0:
                product_entry.stock = 0
                product_entry.save()
            elif new_stock == 0:
                product_entry.stock = 0
                product_entry.save()
                break
            else:
                product_entry.stock = -new_stock
                product_entry.save()
                break

        return ServiceProductDetail.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.service = validated_data.get('service', instance.service)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.employee = validated_data.get('employee', instance.employee)

        if instance.product == validated_data['product']:
            product = instance.product
            product_entry = product.product_entry.latest('created_at')
            quantity = instance.quantity - validated_data['quantity']
            product_entry.stock += quantity
            product_entry.save()
            instance.product = validated_data.get('product', instance.product)

        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

    class Meta:
        model = ServiceProductDetail
        fields = ['id', 'service', 'employee', 'employee_detail', 'product',
                  'product_detail', 'description', 'quantity', 'total_cost']
        read_only_fields = ['total_cost']


class ServiceSerializer(serializers.ModelSerializer):
    # service_products = ServiceProductSerializer(many=True, read_only=True)
    service_products = serializers.SerializerMethodField()
    client_detail = ClientSerializer(source='client', read_only=True)

    class Meta:
        model = Service
        fields = [
            # Create or Update Fields
            'id',
            'client',
            'code',
            'estimated_price',
            'init_date',
            'end_date',
            'observations',
            'name',
            'state',
            # Read only fields
            # Nested Fields
            'service_products',
            'client_detail',
            # Attribute Fields
            'final_price',
        ]

    def get_service_products(self, instance):
        data = instance.service_products.all().order_by('-id')
        return ServiceProductSerializer(data, many=True, read_only=True).data
