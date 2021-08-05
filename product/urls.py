from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^$', views.ListProducts.as_view(), name='list_products'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailProduct.as_view(), name='detail_product'),

    url(r'^sub_product$', views.ListSubProducts.as_view(), name='list_sub_products'),
    url(r'^sub_product/(?P<pk>[0-9]+)/$', views.DetailSubProduct.as_view(), name='detail_sub_product'),

    url(r'^type/$', views.ListTypes.as_view(), name='list_types'),
    url(r'^unit/$', views.ListUnits.as_view(), name='list_units'),
]
