from django.conf.urls import patterns, include, url

from ozio import views
from ozio import views_chart

urlpatterns = patterns('',
    url(r'^$', views.ozio_home, name = 'home'),
    url(r'^test/', views.ozio_test, name = 'test'),
    url(r'^config/', views.ozio_config, name = 'config'),
    url(r'^transaction/', views.ozio_transaction, name = 'transaction'),
    url(r'^map_transaction/', views.ozio_map_transaction, name = 'map_transaction'),
)
