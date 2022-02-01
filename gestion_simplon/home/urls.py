from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home),
    # url(r'', views.login_view),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    # url(r'^addFace/', views.addFace),
    url(r'^welcome/(?P<user_id>\d+)/$', views.welcome),
    url(r'^logout/', views.logout),
    url(r'^dashboard/', views.dashboard),
]
