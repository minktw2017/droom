'''Url Routers'''
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^goods_detail/(?P<p_id>\d+)/(?P<p_no>[-\w]+)/$',
        views.goods_detail,
        name='goods_detail'),
    url(r'^delightroom/$', views.product_list, name='product_list'),
    url(r'^results/$', views.search, name='search'),
    url(r'^(?P<category_slug>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),
    url(r'^(?P<p_id>\d+)/(?P<p_no>[-\w]+)/$',
        views.product_detail,
        name='product_detail'),
]
