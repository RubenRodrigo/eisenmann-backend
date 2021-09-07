import datetime
from django.shortcuts import render
from django.http import Http404

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product, ProductEntry, ProductStock, Type, Unit
from product.serializers import ProductDetailedSerializer, ProductSerializer, ProductEntrySerializer, ProductStockRealSerializer, ProductStockSerializer, TypeSerializer, UnitSerializer


class ListProducts(APIView):
    """
    list all products, or create a new product.
    """

    def get(self, request):
        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailProduct(APIView):
    """
    detail of one product, or create a new product.
    """

    @staticmethod
    def get_object(pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk=pk)
        serializer = ProductDetailedSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(
            product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListProductStock(APIView):
    """
    list all product_stock, or create a new product_stock.
    """

    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        if year is None or month is None:
            today = datetime.datetime.now()
            year = today.year
            month = today.month

        product_stock = ProductStock.objects.filter(
            created_at__year=year, created_at__month=month).order_by('-created_at')
        serializer = ProductStockSerializer(product_stock, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductStockSerializer(
            data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListProductStockOrder(APIView):
    """
    list all product_stock, or create a new product_stock.
    """

    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        if year is None or month is None:
            today = datetime.datetime.now()
            year = today.year
            month = today.month

        product_stock = ProductStock.objects.filter(
            created_at__year=year, created_at__month=month).order_by('stock_total')
        serializer = ProductStockSerializer(product_stock, many=True)
        return Response(serializer.data)


class DetailProductStock(APIView):
    """
    detail of one product_stock.
    """

    @staticmethod
    def get_object(pk):
        try:
            return ProductStock.objects.get(pk=pk)
        except ProductStock.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product_stock = self.get_object(pk=pk)
        serializer = ProductStockSerializer(product_stock)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product_stock = self.get_object(pk)
        serializer = ProductStockSerializer(
            product_stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product_stock = self.get_object(pk)
        product_stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListProductStockReal(APIView):
    """
    list all product_stock, or create a new product_stock.
    """

    def post(self, request, format=None):
        serializer = ProductStockRealSerializer(
            data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductStockReal(APIView):
    """
    detail of one product_stock.
    """

    @staticmethod
    def get_object(pk):
        try:
            return ProductStock.objects.get(pk=pk)
        except ProductStock.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        product_stock = self.get_object(pk)
        serializer = ProductStockRealSerializer(
            product_stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListProductEntries(APIView):
    """
    list all product_entries, or create a new product_entry.
    """

    def get(self, request):
        product_entries = ProductEntry.objects.all().order_by('-created_at')
        serializer = ProductEntrySerializer(product_entries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailProductEntry(APIView):
    """
    detail of one product_entry.
    """

    @staticmethod
    def get_object(pk):
        try:
            return ProductEntry.objects.get(pk=pk)
        except ProductEntry.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product_entry = self.get_object(pk=pk)
        serializer = ProductEntrySerializer(product_entry)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product_entry = self.get_object(pk)
        serializer = ProductEntrySerializer(product_entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product_entry = self.get_object(pk)
        product_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListTypes(APIView):
    """
    list all types, or create a new types.
    """

    def get(self, request):
        types = Type.objects.all()
        serializer = TypeSerializer(types, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailType(APIView):
    """
    detail of one Type.
    """

    @staticmethod
    def get_object(pk):
        try:
            return Type.objects.get(pk=pk)
        except ProductEntry.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        type = self.get_object(pk=pk)
        serializer = TypeSerializer(type)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        type = self.get_object(pk)
        serializer = TypeSerializer(type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        type = self.get_object(pk)
        type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListUnits(APIView):
    """
    list all units, or create a new units.
    """

    def get(self, request):
        units = Unit.objects.all()
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetailUnit(APIView):
    """
    detail of one unit.
    """

    @staticmethod
    def get_object(pk):
        try:
            return Unit.objects.get(pk=pk)
        except Unit.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        unit = self.get_object(pk=pk)
        serializer = UnitSerializer(unit)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        unit = self.get_object(pk)
        serializer = UnitSerializer(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        unit = self.get_object(pk)
        unit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
