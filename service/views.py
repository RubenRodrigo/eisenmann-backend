from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service.models import Service, ServiceProductDetail
from service.serializers import ServiceSerializer, ServiceProductSerializer


class ListServices(APIView):
    """
    list all services, or create a new service.
    """

    def get(self, request):
        services = Service.objects.all().order_by('-id')
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailService(APIView):
    """
    detail of one service, or create a new service.
    """

    @staticmethod
    def get_object(pk):
        try:
            return Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        service = self.get_object(pk=pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        service = self.get_object(pk)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        service = self.get_object(pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListServiceProduct(APIView):
    """
    list all products in services, or create a new service product.
    """

    def get(self, request):
        services_product = ServiceProductDetail.objects.all()
        serializer = ServiceProductSerializer(services_product, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ServiceProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailServiceProduct(APIView):
    """
    detail of one service, or create a new service.
    """

    @staticmethod
    def get_object(pk):
        try:
            return ServiceProductDetail.objects.get(pk=pk)
        except ServiceProductDetail.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        service_product = self.get_object(pk=pk)
        serializer = ServiceProductSerializer(service_product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        service_product = self.get_object(pk)
        serializer = ServiceProductSerializer(
            service_product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        service_product = self.get_object(pk)
        if service_product.service.state is False:
            product = service_product.product
            product_entry = product.product_entry.latest('created_at')
            product_entry.stock += service_product.quantity
            product_entry.save()

        service_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
