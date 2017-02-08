from django.conf.urls import url
from . import views

app_name = 'wishList'

urlpatterns = [
    url(r'^dashboard$', views.index, name='dashboard'),
    url(r'^wish_items/(?P<id>\d+)$', views.show, name='wish_item'),
    url(r'^wish_items/create$', views.create, name='new_item'),
    url(r'^dashboard/update_list/(?P<id>\d+)$', views.update_list, name='update_list'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^add_item/(?P<id>\d+)$', views.add_item, name='add_item'),
    url(r'^remove_item/(?P<id>\d+)$', views.remove_item, name='remove_item'),
    url(r'^delete_item/(?P<id>\d+)$', views.delete_item, name='delete_item'),
]
#
