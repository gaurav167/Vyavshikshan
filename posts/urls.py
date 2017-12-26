from django.urls import path, re_path, include
from . import views

urlpatterns=[
	path('' ,views.index ,name = 'posts'),
	path('<int:pk>/' ,views.page_by_num, name = 'page_by_num'),
	re_path('(?P<num>\d+)/(?P<action>\w+)/' ,views.respond ,name='respond'),
	re_path('(?P<category>\w+)/' ,views.page_by_name, name = 'page_by_name'),
]