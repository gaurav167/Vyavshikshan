from django.urls import path, re_path, include
from . import views

urlpatterns=[
	# Post URLs

	# Create post
	path('post/submit/', views.submit_blog, name='submit_blog'),
	# List all posts
	path('post/all/', views.post_list, name = 'posts'),
	# Edit a post by id(primary key)
	path('post/<int:id>/edit/', views.edit_post, name='edit_post'),
	# Delete post by id(primary key)
	path('post/<int:id>/delete/', views.delete_post, name='delete_post'),
	# Get post by id(primary key)
	path('post/<int:pk>/', views.page_by_num, name = 'page_by_num'),
	# Like/Dislike the post
	re_path('post/(?P<num>\d+)/(?P<action>\w+)/', views.respond, name='respond'),
	# Get all posts by category name
	re_path('post/(?P<category>\w+)/', views.page_by_name, name = 'page_by_name'),

	# Category URLs

	# Create category
	path('category/submit/', views.submit_category, name='submit_category'),
	# List all categories
	path('category/all/', views.all_categs, name='all_categs'),
	# Like/Dislike the category by name
	re_path('category/<int:id>/(?P<action>\w+)/', views.category_respond, name='category_respond'),
	# Delete category by id
	path('category/<int:id>/delete/', views.delete_categ, name='delete_categ'),
]