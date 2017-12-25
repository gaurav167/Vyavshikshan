from django.urls import path, re_path, include
from . import views

urlpatterns=[
	path('' ,views.index ,name = 'posts'),
	path('home/', include('home.urls')),
	path('write/', include('write.urls')),
	re_path('(?P<pk>\d+)/' ,views.page_by_num, name = 'page_by_num'),
	re_path('(?P<category>\w+)/' ,views.page_by_name, name = 'page_by_name'),
	re_path('(?P<num>\d+)/like/' ,views.liked ,name='likePost'),
	re_path('(?P<num>\d+)/dislike/' ,views.disliked ,name='dislikePost'),
]