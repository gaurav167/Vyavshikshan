from django.urls import path
from . import views

urlpatterns=[
	path('' ,views.index ,name = 'contact'),
	path('submit/' ,views.submit ,name = 'contact_submit'),
]