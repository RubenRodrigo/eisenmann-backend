from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^$', views.ListProducts.as_view(), name='list_products'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailProduct.as_view(),
        name='detail_product'),

    url(r'^product_entry/$', views.ListProductEntries.as_view(),
        name='list_product_entries'),
    url(r'^product_entry/(?P<pk>[0-9]+)/$',
        views.DetailProductEntry.as_view(), name='detail_product_entry'),

    url(r'^type/$', views.ListTypes.as_view(), name='list_types'),
    url(r'^unit/$', views.ListUnits.as_view(), name='list_units'),
]
