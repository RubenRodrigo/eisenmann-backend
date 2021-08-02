from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ListServices.as_view(), name='list_services'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailService.as_view(), name='detail_service'),
    url(r'^service_product/$', views.ListServiceProduct.as_view(), name='list_service_product'),
    url(r'^service_product/(?P<pk>[0-9]+)/$', views.DetailServiceProduct.as_view(), name='detail_service_product'),
]
