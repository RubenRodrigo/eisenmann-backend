from django.shortcuts import render
from django.http import Http404

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product, SubProduct, Type, Unit
from product.serializers import ProductSerializer, SubProductSerializer, TypeSerializer, UnitSerializer


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
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListSubProducts(APIView):
    """
    list all sub_products, or create a new sub_product.
    """

    def get(self, request):
        sub_products = SubProduct.objects.all().order_by('-created_at')
        serializer = SubProductSerializer(sub_products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SubProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailSubProduct(APIView):
    """
    detail of one sub_product, or create a new sub_product.
    """

    @staticmethod
    def get_object(pk):
        try:
            return SubProduct.objects.get(pk=pk)
        except SubProduct.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        sub_product = self.get_object(pk=pk)
        serializer = SubProductSerializer(sub_product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        sub_product = self.get_object(pk)
        serializer = SubProductSerializer(sub_product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        sub_product = self.get_object(pk)
        sub_product.delete()
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
