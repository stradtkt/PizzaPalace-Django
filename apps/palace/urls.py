from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^order-now$', views.order_now),
    url(r'^login-page$', views.login_page),
    url(r'^register-page$', views.register_page),
]