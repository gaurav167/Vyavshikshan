from django.urls import path, re_path
from . import views

urlpatterns=[

	# Manage Tests URLs
	
	# Start Test Session
	path('start/', views.starttest, name='starttest'),
	# Stop Test Session and Evaluate Score
	path('stop/', views.stoptest, name='stoptest'),
	

	# Question URL

	# Add new question
	path('question/add/', views.add_ques, name='add_ques'),
	# Get all questions
	path('question/all/', views.ques_all, name='ques_all'),
	# Edit question
	path('question/edit/<int:id>/', views.edit_ques, name='edit_ques'),
	# Delete question
	path('question/delete/<int:id>/', views.delete_ques, name='delete_ques'),
]