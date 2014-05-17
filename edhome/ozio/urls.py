from django.conf.urls import patterns, include, url

from ozio import views

urlpatterns = patterns('',
    url(r'^$', views.ozio_home, name = 'home'),
    url(r'^test/', views.ozio_test, name = 'test'),
    url(r'^config/', views.ozio_config, name = 'config'),
    url(r'^transaction/', views.ozio_transaction, name = 'transaction'),
    
    url(r'^map_transaction/', views.ozio_map_transaction, name = 'map_transaction'),
    url(r'^add_manual_csv/(?P<file_name>[^/]+)/$', views.ozio_add_manual_csv, name = 'add_manual_csv'),
    url(r'^add_manual_transaction/', views.ozio_add_manual_transaction, name = 'add_manual_transaction'),
    url(r'^split_transaction/', views.ozio_split_transaction, name = 'split_transaction'),
    url(r'^on_object_delete/(?P<obj_name>[^/]+)/(?P<obj_id>[^/]+)/$', views.ozio_on_object_delete, name = 'on_obj_delete'),
    ###
    url(r'^add_or_edit/(?P<obj_type>[^/]+)/(?P<obj_id>[^/]+)/$', views.ozio_add_or_edit, name = 'add_or_edit'),
)
