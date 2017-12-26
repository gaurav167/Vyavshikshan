from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Post, Category
from django.http import HttpResponse, Http404


def index(request):
	posts = Post.objects.order_by('-published_date')
	data = serializers.serialize('json', posts)
	return JsonResponse(data, safe=False)

def page_by_num(request,pk):
	posts = [get_object_or_404(Post, pk=pk)]
	data = serializers.serialize('json', posts)
	return JsonResponse(data, safe=False)

def page_by_name(request,category):
	categ = get_object_or_404(Category, name=category.lower())
	posts = Post.objects.filter(categories=categ.id)
	if len(posts) == 0:
		raise Http404
	data = serializers.serialize('json', posts)
	return JsonResponse(data, safe=False)

def respond(request,num,action):
	post = get_object_or_404(Post, pk=num)
	if action == 'like':
		post.likes += 1
	if action == 'dislike':
		post.dislikes += 1
	post.save()
	return JsonResponse({"status":"success"})