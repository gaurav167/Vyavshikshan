from django.core import serializers
from django.http import JsonResponse
from .models import Post, Category
from django.http import QueryDict,HttpResponse
from django.contrib.auth.models import User


# Create a new Post
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
		return JsonResponse({'error':'Only available via POST.','status':'403'})

# Show all Posts
def post_list(request):
	if request.method == "GET":
		posts = Post.objects.order_by('-published_date')
		data = serializers.serialize('json', posts)
		return JsonResponse(data, safe=False)
	else:
		return JsonResponse({'error':'Only available via GET.','status':'403'})

# Show post by primary key
def page_by_num(request,pk):
	if request.method == "GET":
		try:
			post = [Post.objects.get(pk=pk)]
		except:
			return JsonResponse({'error':'Post not Found','status':'404'})
		data = serializers.serialize('json', post)
		return JsonResponse(data, safe=False)
	else:
		return JsonResponse({'error':'Only available via GET.','status':'403'})

# Show posts by category name
def page_by_name(request,category):
	if request.method == "GET":
		try:
			categ = Category.objects.get(name=category.lower())
		except:
			return JsonResponse({'error':'Category not Found','status':'404'})
		try:
			posts = Post.objects.get(categories=categ.id)
		except:
			return JsonResponse({'error':'Not Found','status':'404'})
		data = serializers.serialize('json', posts)
		return JsonResponse(data, safe=False)
	else:
		return JsonResponse({'error':'Only available via GET.','status':'403'})

# Like/Dislike post
def respond(request,num,action):
	if request.method == "PUT":
		try:
			try:
				post = Post.objects.get(pk=num)
			except:
				return JsonResponse({'error':'Post not Found','status':'404'})
			if action == 'like':
				post.likes += 1
			if action == 'dislike':
				post.dislikes += 1
			post.save()
			return JsonResponse({"status":"success"})
		except:
			return JsonResponse({'status':'failed','message':'None'})
	else:
		return JsonResponse({'error':'Only available via PUT.','status':'403'})

# Edit a post
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
		return JsonResponse({'error':'Only available via PATCH.','status':'403'})

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
		return JsonResponse({'error':'Only available via DELETE.','status':'403'})




# Create a category
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
		return JsonResponse({'error':'Only available via POST.','status':'403'})

# Get all categories
def all_categs(request):
	if request.method == "GET":
		categories = Category.objects.order_by('name')
		data = serializers.serialize('json', categories)
		return JsonResponse(data, safe=False)
	else:
		return JsonResponse({'error':'Only available via GET.','status':'403'})

# Like/Dislike a category
def category_respond(request,id,action):
	if request.method == "PUT":
		try:
			categ = Category.objects.get(pk=id)
		except:
			return JsonResponse({'error':'Not Found','status':'404'})
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
		return JsonResponse({'error':'Only available via PUT.','status':'403'})

# Delete a category
def delete_categ(request,id):
	if request.method == 'DELETE':
		try:
			categ = Category.objects.get(pk=id)
		except:
			return JsonResponse({'status':'failed','message':'Category does not exist'})
		try:
			categ.delete()
		except:
			return JsonResponse({'status':'failed','message':'Cannot delete category at the moment.'})
	else:
		return JsonResponse({'error':'Only available via DELETE.','status':'403'})
