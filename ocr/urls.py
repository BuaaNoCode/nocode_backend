from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^project/$', views.generalPro)
    url(r'^project/(\d+)/$', views.detailPro),
    url(r'^project/(?P<p1>\d+)/(?P<p2>\d+)/$', views.result),