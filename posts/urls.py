from django.conf.urls import url, include
from . import views

urlpatterns=[
	# Post URLs

	# Create post
	url('post/submit/', views.submit_blog, name='submit_blog'),
	# List all posts
	url('post/all/', views.post_list, name = 'posts'),
	# Edit a post by id(primary key)
	url('post/(?P<id>\d+)/edit/', views.edit_post, name='edit_post'),
	# Delete post by id(primary key)
	url('post/(?P<id>\d+)/delete/', views.delete_post, name='delete_post'),
	# Get post by id(primary key)
	url('post/(?P<pk>\d+)/', views.page_by_num, name = 'page_by_num'),
	# Like/Dislike the post
	url('post/(?P<num>\d+)/(?P<action>\w+)/', views.respond, name='respond'),
	# Get all posts by category name
	url('post/(?P<category>\w+)/', views.page_by_name, name = 'page_by_name'),

	# Category URLs

	# Create category
	url('category/submit/', views.submit_category, name='submit_category'),
	# List all categories
	url('category/all/', views.all_categs, name='all_categs'),
	# Like/Dislike the category by name
	url('category/(?P<id>\d+)/(?P<action>\w+)/', views.category_respond, name='category_respond'),
	# Delete category by id
	url('category/(?P<id>\d+)/delete/', views.delete_categ, name='delete_categ'),
]