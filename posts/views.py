from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Post, Category
from django.http import HttpResponse, Http404, QueryDict


# Show all Posts
def index(request):
	if request.method == "GET":
		posts = Post.objects.order_by('-published_date')
		data = serializers.serialize('json', posts)
		return JsonResponse(data, safe=False)
	else:
		raise "Only available via GET."

# Show post by primary key
def page_by_num(request,pk):
	if request.method == "GET":
		posts = [get_object_or_404(Post, pk=pk)]
		data = serializers.serialize('json', posts)
		return JsonResponse(data, safe=False)
	else:
		raise "Only available via GET."

# Show posts by category name
def page_by_name(request,category):
	if request.method == "GET":
		categ = get_object_or_404(Category, name=category.lower())
		posts = Post.objects.filter(categories=categ.id)
		if len(posts) == 0:
			raise Http404
		data = serializers.serialize('json', posts)
		return JsonResponse(data, safe=False)
	else:
		raise "Only available via GET."

# Like/Dislike post
def respond(request,num,action):
	if request.method == "PUT":
		try:
			post = get_object_or_404(Post, pk=num)
			if action == 'like':
				post.likes += 1
			if action == 'dislike':
				post.dislikes += 1
			post.save()
			return JsonResponse({"status":"success"})
		except:
			return JsonResponse({'status':'failed','message':'None'})
	else:
		raise "Only available via PUT."

# Create a new Post
def submit_blog(request):
	if request.method == "POST":
		try:
			try:
				author = request.POST.get('author')
				title = request.POST.get('title')
				subtitle = request.POST.get('subtitle')
				text = request.POST.get('text')
				image = request.FILES['image']
				categories = request.POST.get('category')
			except:
				return JsonResponse({'status':'failed', 'message':'Invalid POST data.'})
			try:
				categ = Category.objects.get(name=categories)
			except:
				categ = Category.objects.create(name=categories)
			try:
				new_post = Post.objects.create(author=author, title=title, subtitle=subtitle, text=text, categories=categ.id, image=image)
			except:
				return JsonResponse({'status':'failed', 'message':"Couldn't create Post object"})
		except:
			return JsonResponse({'status':'failed','message':'None'})
	else:
		raise "Only available via POST."

# Edit a post
def edit_post(request,id):
	if request.message == "PATCH":
		try:
			post = Post.objects.get(id=id)
		except:
			return JsonResponse({'status':'failed','message':'No post with id='+str(id)})
		try:
			data = QueryDict(request.body).dict()
			for field in data.keys():
				if field == 'title':
					post.title = data[field]
				if field == 'subtitle':
					post.subtitle = data[field]
				if field == 'text':
					post.text = data[field]
				if field == 'category':
					try:
						categ = Category.objects.get(name=data[field])
					except:
						categ = Category.objects.create(name=data[field])
					post.categories = categ.id
			try:
				img = request.FILES['image']
				post.image = img
			except:
				pass
			post.save()
		except:			
			return JsonResponse({'status':'failed','message':'Cannot update post.'})
	else:
		raise "Only available via PATCH."

# Delete a post
def delete_post(request,id):
	if request.method == 'DELETE':
		try:
			post = Post.objects.get(id=id)
		except:
			return JsonResponse({'status':'failed','message':'Post does not exist'})
		try:
			post.delete()
		except:
			return JsonResponse({'status':'failed','message':'Cannot delete post at the moment.'})
	else:
		raise "Only available via DELETE."


# Create a category
def submit_category(request,name):
	if request.method == "POST":
		try:
			categ = Category.objects.get(name=categories)
			return JsonResponse({'status':'failed','message':'Category already exists'})
		except:
			categ = Category.objects.create(name=name)
			return JsonResponse({"status":"success"})
	else:
		raise "Only available via POST."

# Get all categories
def all_categs(request):
	if request.method == "GET":
		categories = sorted(Category.objects.all(), key=str.lower)
		data = serializers.serialize('json', categories)
		return JsonResponse(data, safe=False)
	else:
		raise "Only available via GET."

# Like/Dislike a category
def category_respond(request,name,action):
	if request.method == "PUT":
		try:
			categ = Category.objects.get(name=categories)
		except:
			raise Http404
		try:
			if action == 'like':
				categ.likes += 1
			elif action == 'dislike':
				categ.dislikes += 1
			categ.save()
			return JsonResponse({"status":"success"})
		except:
			return JsonResponse({'status':'failed','message':'None'})
	else:
		raise "Only available via PUT."

# Delete a category
def delete_categ(request,id):
	if request.method == 'DELETE':
		try:
			categ = Category.objects.get(id=id)
		except:
			return JsonResponse({'status':'failed','message':'Category does not exist'})
		try:
			categ.delete()
		except:
			return JsonResponse({'status':'failed','message':'Cannot delete category at the moment.'})
	else:
		raise "Only available via DELETE."
