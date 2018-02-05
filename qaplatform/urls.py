from django.conf.urls import url
from . import views

urlpatterns=[

	# Manage Tests URLs
	
	# Start Test Session
	url('start/', views.starttest, name='starttest'),
	# Stop Test Session and Evaluate Score
	url('stop/', views.stoptest, name='stoptest'),
	# Revise previous solutions
	url('revise/(?P<sess_id>\d+)/', views.revise, name='revise'),

	# Question URL

	# Add new question
	url('question/add/', views.add_ques, name='add_ques'),
	# Get all questions
	url('question/all/', views.ques_all, name='ques_all'),
	# Edit question
	url('question/edit/(?P<id>\d+)/', views.edit_ques, name='edit_ques'),
	# Delete question
	url('question/delete/(?P<id>\d+)/', views.delete_ques, name='delete_ques'),
]