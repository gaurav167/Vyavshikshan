from django.core import serializers
from django.http import JsonResponse
from .models import Post, Category
from django.http import QueryDict,HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt



# Create a new Post
@csrf_exempt
def submit_blog(request):
	if request.method == "POST":
		try:
			try:
				author = request.POST.get('author')
				title = request.POST.get('title')
				subtitle = request.POST.get('subtitle')
				text = request.POST.get('text')
				categories = request.POST.get('category').lower()
				try:
					image = request.FILES['image']
				except:
					image = None
			except:
				return JsonResponse({'status':'failed', 'message':'Invalid POST data.'})
			try:
				user = User.objects.get(username=author)
			except:
				return JsonResponse({'status':'failed','message':'User does not exist.'})
			try:
				categ, created = Category.objects.get_or_create(name=categories)
				if created:
					categ = Category.objects.get(name=categories)
			except:
				return JsonResponse({'status':'failed', 'message':"Couldn't create Category object"})					
			try:
				data={
				'author':user,
				'title':title,
				'subtitle':subtitle,
				'text':text,
				'categories':categ,
				}
				new_post = Post(**data)
				new_post.publish()
				return JsonResponse({'status':'success'})
			except:
				return JsonResponse({'status':'failed', 'message':"Couldn't create Post object"})
		except:
			return JsonResponse({'status':'failed','message':'None'})
	else:
		return JsonResponse({'error':'Only available via POST.','status_code':'400'})

# Show all Posts
def post_list(request):
	if request.method == "GET":
		posts = Post.objects.order_by('-published_date')
		data = serializers.serialize('json', posts)
		return JsonResponse(data, safe=False)
	else:
		return JsonResponse({'error':'Only available via GET.','status_code':'400'})

# Show post by primary key
def page_by_num(request,pk):
	if request.method == "GET":
		try:
			post = [Post.objects.get(pk=pk)]
		except:
			return JsonResponse({'error':'Post not Found','status_code':'404'})
		data = serializers.serialize('json', post)
		return JsonResponse(data, safe=False)
	else:
		return JsonResponse({'error':'Only available via GET.','status_code':'400'})

# Show posts by category name
def page_by_name(request,category):
	if request.method == "GET":
		try:
			categ = Category.objects.get(name=category.lower())
		except:
			return JsonResponse({'error':'Category not Found','status_code':'404'})
		try:
			posts = Post.objects.filter(categories=categ.id)
			if len(posts) == 0:
				return JsonResponse({'status':'failed','message':'No post in this category.'})
		except:
			return JsonResponse({'error':'Not Found','status_code':'404'})
		data = serializers.serialize('json', posts)
		return JsonResponse(data, safe=False)
	else:
		return JsonResponse({'error':'Only available via GET.','status_code':'400'})

# Like/Dislike post
def respond(request,num,action):
	if request.method == "PUT":
		try:
			try:
				post = Post.objects.get(pk=num)
			except:
				return JsonResponse({'error':'Post not Found','status_code':'404'})
			action = action.lower()
			if action == 'like':
				post.likes += 1
			elif action == 'dislike':
				post.dislikes += 1
			else:
				return JsonResponse({'status':'failed','message':'Unknown action.'})
			post.save()
			return JsonResponse({"status":"success"})
		except:
			return JsonResponse({'status':'failed','message':'None'})
	else:
		return JsonResponse({'error':'Only available via PUT.','status_code':'400'})

# Edit a post
@csrf_exempt
def edit_post(request,id):
	if request.method == "POST":
		try:
			post = Post.objects.get(id=id)
		except:
			return JsonResponse({'status':'failed','message':'No post with id='+str(id)})
		try:
			# data = request.POST
			querydict = QueryDict('', mutable=True)
			for key in request.POST.iteritems():
			    postlist = post[key].split(',')
			    querydict.setlist(key, postlist)
			# for field in data.keys():
			# 	if field == 'title':
			# 		post.title = data[field]
			# 	if field == 'subtitle':
			# 		post.subtitle = data[field]
			# 	if field == 'text':
			# 		post.text = data[field]
			# 	if field == 'category':
			# 		try:
			# 			categ = Category.objects.get(name=data[field])
			# 		except:
			# 			categ = Category.objects.create(name=data[field])
			# 		post.categories = categ.id
			# try:
			# 	img = request.FILES['image']
			# 	post.image = img
			# except:
			# 	pass
			Post.objects.filter(id=id).update(**querydict)
			# post.save()
			return HttpResponse(data)
		except Exception as e:
			return HttpResponse(e)
		# except:			
		# 	return JsonResponse({'status':'failed','message':'Cannot update post.'})
	else:
		return JsonResponse({'error':'Only available via PATCH.','status_code':'400'})

# Delete a post
def delete_post(request,id):
	if request.method == 'DELETE':
		try:
			post = Post.objects.get(id=id)
		except:
			return JsonResponse({'status':'failed','message':'Post does not exist'})
		try:
			post.delete()
			return JsonResponse({'status':'success'})
		except:
			return JsonResponse({'status':'failed','message':'Cannot delete post at the moment.'})
	else:
		return JsonResponse({'error':'Only available via DELETE.','status_code':'400'})



# Create a category
@csrf_exempt
def submit_category(request):
	if request.method == "POST":
		try:
			name = request.POST.get('category').lower()
		except:
			return JsonResponse({'status':'failed','message':'Invalid POST data.'})
		try:
			categ = Category.objects.get(name=name)
			return JsonResponse({'status':'failed','message':'Category {} already exists.'.format(name)})
		except:
			try:
				categ = Category.objects.create(name=name)
			except:
				return JsonResponse({'status':'failed','message':'Cannot create Category object.'})
			else:
				return JsonResponse({"status":"success"})
	else:
		return JsonResponse({'error':'Only available via POST.','status_code':'400'})

# Get all categories
def all_categs(request):
	if request.method == "GET":
		try:
			categories = Category.objects.order_by('name')
		except:
			return JsonResponse({'status':'failed','message':'No categories'})
		data = serializers.serialize('json', categories)
		return JsonResponse(data, safe=False)
	else:
		return JsonResponse({'error':'Only available via GET.','status_code':'400'})

# Get category by name
def get_categ(request,name):
	if request.method == "GET":
		try:
			categ = [Category.objects.get(name=name.lower())]
		except:
			return JsonResponse({'status':'failed','message':'No such category'})
		data = serializers.serialize('json', categ)
		return JsonResponse(data, safe=False)
	else:
		return JsonResponse({'error':'Only available via GET.','status_code':'400'})

# Like/Dislike a category
def category_respond(request,name,action):
	if request.method == "PUT":
		try:
			categ = Category.objects.get(name=name.lower())
		except:
			return JsonResponse({'error':'Not Found','status_code':'404'})
		try:
			action = action.lower()
			if action == 'like':
				categ.likes += 1
			elif action == 'dislike':
				categ.dislikes += 1
			categ.save()
			return JsonResponse({"status":"success"})
		except:
			return JsonResponse({'status':'failed','message':'None'})
	else:
		return JsonResponse({'error':'Only available via PUT.','status_code':'400'})

# Delete a category
def delete_categ(request,id):
	if request.method == 'DELETE':
		try:
			categ = Category.objects.get(pk=id)
		except:
			return JsonResponse({'status':'failed','message':'Category does not exist'})
		try:
			categ.delete()
			return JsonResponse({'status':'success'})
		except:
			return JsonResponse({'status':'failed','message':'Cannot delete category at the moment.'})
	else:
		return JsonResponse({'error':'Only available via DELETE.','status_code':'400'})
