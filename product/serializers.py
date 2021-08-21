from django.shortcuts import get_object_or_404
from rest_framework import serializers
import datetime

from product.models import Product, ProductEntry, ProductStock, Type, Unit


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = ['id',  'name', 'description']


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = ['id',  'name', 'description', 'abr']


class ProductEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductEntry
        fields = ['id', 'product', 'init_stock', 'stock', 'description',
                  'unit_price', 'created_at', 'updated_at', 'total_cost']


class ProductSerializer(serializers.ModelSerializer):

    type_detail = TypeSerializer(source='type', read_only=True)
    unit_detail = UnitSerializer(source='unit', read_only=True)

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
            'total_price',

            # 'product_entry',
            'type_detail',
            'unit_detail'
        ]


class ProductStockSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = [
            # Create or Update Fields
            'id',
            'product',
            'init_stock',
            'real_stock',
            'state',
            'medium_value',
            'minium_value',

            # Read only fields
            'created_at',
            'updated_at',

            # Attribute Fields
            'total_stock',
            'total_stock_entries',
            'total_stock_price',
            'difference_stock',
            'current_price',
        ]


class ProductDetailedSerializer(serializers.ModelSerializer):

    type_detail = TypeSerializer(source='type', read_only=True)
    unit_detail = UnitSerializer(source='unit', read_only=True)
    product_stock = ProductStockSimpleSerializer(many=True, read_only=True)

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
            'total_price',

            # Nested Fields
            'product_stock',
            # 'product_entry',
            'type_detail',
            'unit_detail'
        ]


class ProductStockSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    product_entry = ProductEntrySerializer(many=True, read_only=True)

    class Meta:
        model = ProductStock
        fields = [
            # Create or Update Fields
            'id',
            'product',
            'init_stock',
            'real_stock',
            'state',
            'medium_value',
            'minium_value',
            'stock_total',

            # Read only fields
            'created_at',
            'updated_at',

            # Nested Fields
            'product_detail',
            'product_entry',

            # Attribute Fields
            'total_stock',
            'total_stock_entries',
            'total_stock_price',
            'difference_stock',
            'current_price',
        ]

    def validate_product(self, value):
        today = datetime.datetime.now()
        queryset = ProductStock.objects.filter(product=value).filter(
            created_at__year=today.year, created_at__month=today.month)

        if queryset.exists():
            raise serializers.ValidationError(
                {"product": "Ya hay otro producto_stock para este mes"}
            )
        return value

    def create(self, validated_data):
        today = datetime.datetime.now()
        created_at = today
        return ProductStock.objects.create(created_at=created_at, **validated_data)


class ProductStockRealSerializer(serializers.ModelSerializer):

    # custom field that will be used to get previous productstock object
    prev_stock = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = ProductStock
        fields = ['prev_stock']

    # validate prev_stock.
    #
    def validate_prev_stock(self, value):
        prev_stock = get_object_or_404(ProductStock, pk=value)
        created_at = add_months(prev_stock.created_at, 1)
        queryset = ProductStock.objects.filter(product=prev_stock.product).filter(
            created_at__year=created_at.year, created_at__month=created_at.month)

        if not prev_stock.product_entry.exists():
            raise serializers.ValidationError(
                {"prev": "El producto previo no tiene entradas"}
            )

        if queryset.exists():
            raise serializers.ValidationError(
                {"prev": "Ya hay otro producto_stock para el siguiente mes"})

        return prev_stock

    def create(self, validated_data):
        prev_stock = validated_data.pop('prev_stock')
        created_at = add_months(prev_stock.created_at, 1)
        init_stock = prev_stock.real_stock

        product_stock = ProductStock.objects.create(
            created_at=created_at,
            product=prev_stock.product,
            init_stock=init_stock,
        )

        if prev_stock.product_entry.exists():
            current_price = prev_stock.current_price
            ProductEntry.objects.create(
                product=product_stock,
                init_stock=init_stock,
                stock=init_stock,
                description="Primera entrada",
                unit_price=current_price)

        return product_stock


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = 1
    return datetime.date(year, month, day)
