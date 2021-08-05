from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ListEmployees.as_view(), name='list_employees'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailEmployee.as_view(), name='detail_employee'),
]

