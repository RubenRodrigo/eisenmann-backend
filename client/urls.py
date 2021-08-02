from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ListClients.as_view(), name='list_clients'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailClient.as_view(), name='detail_client'),
]
