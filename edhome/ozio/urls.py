from django.conf.urls import patterns, include, url

from ozio import views

urlpatterns = patterns('',
    url(r'^$', views.ozio_home, name = 'home'),
    url(r'^test/', views.ozio_test, name = 'test'),
)
