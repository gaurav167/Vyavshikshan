from django.conf.urls import url
from . import views

urlpatterns = [
    url('login/', views.login, name='login'),
    url('logout/', views.logout, name='logout'),
    url('register/', views.register, name='register'),
    url('get/(?P<username>\w+)/', views.get_user, name='get_user'),
    url('change/password/(?P<username>\w+)/', views.change_pass, name='change_pass'),
]