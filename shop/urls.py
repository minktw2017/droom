from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^delightroom/$', views.product_list, name='product_list'),
    url(r'^results/$', views.search, name='search'),
    url(r'^(?P<category_slug>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<no>[-\w]+)/$',
        views.product_detail,
        name='product_detail'),
]
