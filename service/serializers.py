from rest_framework import serializers

from client.serializers import ClientSerializer
from product.serializers import ProductSerializer
from service.models import Service, ServiceProductDetail
from employee.serializers import EmployeeSerializer


# Serializers para los servicios


class ServiceProductSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    employee_detail = EmployeeSerializer(source='employee', read_only=True)

    def validate(self, data):
        if data['quantity'] > data['product'].total_stock:
            raise serializers.ValidationError("Not enough stock")
        return data

    def create(self, validated_data):
        quantity = validated_data['quantity']
        product = validated_data['product']
        sub_products = product.sub_product.all().order_by('created_at')

        new_stock = quantity
        
        for sub_product in sub_products:
            new_stock = new_stock - sub_product.stock 
            if new_stock > 0:
                sub_product.stock = 0
                sub_product.save() 
            elif new_stock == 0:
                sub_product.stock = 0
                sub_product.save() 
                break
            else:
                sub_product.stock = -new_stock
                sub_product.save()
                break

        return ServiceProductDetail.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.service = validated_data.get('service', instance.service)
        instance.description = validated_data.get('description', instance.description)
        instance.employee = validated_data.get('employee', instance.employee)

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
            sub_product = product.sub_product.latest('created_at')
            quantity = instance.quantity - validated_data['quantity']
            sub_product.stock += quantity
            sub_product.save()
            instance.product = validated_data.get('product', instance.product)
        # else:
        #     current_product = instance.product
        #     sub_product = current_product.sub_product.latest('created_at')
        #     sub_product.stock += instance.quantity
        #     sub_product.save()

        #     new_product = validated_data['product']
        #     # new_product.stock -= quantity
        #     # new_product.save()

        #     new_sub_products = new_product.sub_product.all().order_by('created_at')
        #     quantity = validated_data['quantity']

        #     new_stock = quantity
            
        #     for new_sub_product in new_sub_products:
        #         new_stock = new_stock - new_sub_product.stock 
        #         if new_stock > 0:
        #             new_sub_product.stock = 0
        #             new_sub_product.save() 
        #         elif new_stock == 0:
        #             new_sub_product.stock = 0
        #             new_sub_product.save() 
        #             break
        #         else:
        #             new_sub_product.stock = -new_stock
        #             new_sub_product.save()
        #             break

        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

    class Meta:
        model = ServiceProductDetail
        fields = ['id', 'service', 'employee', 'employee_detail', 'product', 'product_detail', 'description', 'quantity', 'total_cost']
        read_only_fields = ['total_cost']


class ServiceSerializer(serializers.ModelSerializer):
    # service_products = ServiceProductSerializer(many=True, read_only=True)
    service_products = serializers.SerializerMethodField()
    client_detail = ClientSerializer(source='client', read_only=True)

    class Meta:
        model = Service
        fields = [
            'id',
            'client',
            'code',
            'estimated_price',
            'final_price',
            'init_date',
            'end_date',
            'observations',
            'name',
            'state',
            'client_detail',
            'service_products',
        ]

    def get_service_products(self, instance):
        data = instance.service_products.all().order_by('-id')
        return ServiceProductSerializer(data, many=True, read_only=True).data
