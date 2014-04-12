from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from edhome import views
from ozio import views_class

# REST Framework
from rest_framework import routers 
router = routers.DefaultRouter() 
router.register('type', views_class.TypeViewSet)
router.register('cate', views_class.CateViewSet)
router.register('subcate', views_class.SubCateViewSet)
router.register('keyword', views_class.KeywordViewSet)
router.register('sourcefile', views_class.SourceFileViewSet)
router.register('transaction', views_class.TransactionViewSet)
router.register('transaction_filter', views_class.TransactionFilterViewSet)
router.register('filter_sql', views_class.FilterSQLViewSet)
# REST Framework ===========

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'edhome.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.edhome, name = 'home'),
    url(r'^login/', views.login, name = 'login'),
    url(r'^logout/', views.logout, name = 'logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ozio/', include('ozio.urls', namespace='ozio')),
    
    url(r'^API/', include(router.urls)), # REST Framework
)
