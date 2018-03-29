from django.contrib.auth import authenticate
from django.contrib.auth  import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import UserProfile


@csrf_exempt
def login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return JsonResponse({'status':'success'})
		else:
			return JsonResponse({'status':'failed', 'message':'Invalid User credentials.'})
	else:
		return JsonResponse({'error':'Only available via POST.','status_code':'400'})


def logout(request):
	try:
		logout(request)
		return JsonResponse({'status':'success'})
	except:
		return JsonResponse({'status':'failed', 'message':"Coudn't log out at the moment."})


@csrf_exempt
def register(request):
	if request.method == "POST":
		try:
			username = request.POST['username']
			password = request.POST['password']
			email = request.POST['email']
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			city = request.POST['city']
			state = request.POST['state']
			pincode = request.POST['pincode']
		except:
			return JsonResponse({'status':'failed', 'message':'Invalid POST data.'})
		try:
			if len(User.objects.filter(username=username)) > 0:
				return JsonResponse({'status':'failed', 'message':'Username already taken.'})

			usr = User(first_name=first_name, last_name=last_name, email=email, username=username, is_staff=False, is_superuser=False)
			usr.set_unusable_password()
			usr.set_password(password)
			usr.save()
			user = UserProfile.objects.create(user=usr, city=city, state=state, pincode=pincode)
			return JsonResponse({'status':'success'})
		except:
			return JsonResponse({'status':'failed', 'message':"Coudn't register at the moment."})

	else:
		return JsonResponse({'error':'Only available via POST.','status_code':'400'})


def get_user(request, username):
	if request.method == "GET":
		try:
			usr = User.objects.get(username=username)
			profile = UserProfile.objects.get(user=usr)
		except:
			return JsonResponse({'status':'failed', 'message':"No user found."})
		try:
			data = {
			'username' : usr.get_username(),
			'full_name' : usr.get_full_name(),
			'email' : usr.email,
			'city' : profile.city,
			'state' : profile.state,
			'pincode' : profile.pincode
			}

			return JsonResponse(data)
		except:
			return JsonResponse({'status':'failed', 'message':"Can't contact server at the moment."})
	else:
		return JsonResponse({'error':'Only available via GET.','status_code':'400'})


@csrf_exempt
@login_required
def change_pass(request, username):
	if request.method == "POST":
		try:
			usr = User.objects.get(username=username)
			if usr.is_authenticated and usr.check_password(request.POST['old_password']):
				usr.set_password(request.POST['new_password'])
				return JsonResponse({'status':'success'})
			else:
				return JsonResponse({'status':'failed', 'message':"User not Authenticated."})
		except:
			return JsonResponse({'status':'failed', 'message':"No user found."})
	else:
		return JsonResponse({'error':'Only available via POST.','status_code':'400'})