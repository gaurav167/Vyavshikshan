from django.conf.urls import url
from . import views

urlpatterns = [
    url('login/', views.login, name='login'),
    url('logout/', views.logout, name='logout'),
    url('register/', views.register, name='register'),
]