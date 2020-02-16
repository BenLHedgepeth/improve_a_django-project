from django.conf.urls import url, include
from django.contrib.auth import views
from django.conf import settings
from . import views

app_name = "menu"
urlpatterns = [
    url(r'^$', views.menu_list, name='menu_list'),
    url(r'^menu/(?P<pk>\d+)/edit/$', views.edit_menu, name='menu_edit'),
    url(r'^menu/(?P<pk>\d+)/$', views.menu_detail, name='menu_detail'),
    url(r'^menu/item/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
    url(r'^menu/new/$', views.create_new_menu, name='menu_new')
]

