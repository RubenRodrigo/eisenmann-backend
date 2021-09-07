from django.conf.urls import url

from . import views
urlpatterns = [
    # List or Detail of the product
    url(r'^$', views.ListProducts.as_view(), name='list_products'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailProduct.as_view(),
        name='detail_product'),

    # List or Detail of the product stock
    url(r'^product_stock/$', views.ListProductStock.as_view(),
        name='list_product_stock'),
    url(r'^product_stock/(?P<pk>[0-9]+)/$',
        views.DetailProductStock.as_view(), name='detail_product_stock'),

    url(r'^product_stock_order/$', views.ListProductStockOrder.as_view()),

    # Real stock of the product
    url(r'^product_stock_real/$', views.ListProductStockReal.as_view()),
    url(r'^product_stock_real/(?P<pk>[0-9]+)/$',
        views.ProductStockReal.as_view()),

    url(r'^product_entry/$', views.ListProductEntries.as_view(),
        name='list_product_entries'),
    url(r'^product_entry/(?P<pk>[0-9]+)/$',
        views.DetailProductEntry.as_view(), name='detail_product_entry'),

    url(r'^type/$', views.ListTypes.as_view(), name='list_types'),
    url(r'^type/(?P<pk>[0-9]+)/$', views.DetailType.as_view()),

    url(r'^unit/$', views.ListUnits.as_view(), name='list_units'),
    url(r'^unit/(?P<pk>[0-9]+)/$', views.DetailUnit.as_view()),
]
