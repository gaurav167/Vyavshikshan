from django.shortcuts import render
from django.http import QueryDict,HttpResponse
from django.core import serializers
from django.http import JsonResponse
from .models import Question, Session
from django.views.decorators.csrf import csrf_exempt

def starttest(request):
	pass

def stoptest(request):
	pass

def upload_ques(request):
	pass


def ques_all(request):
	if request.method == "GET":
		try:
			ques = Question.objects.all()
		except:
			return JsonResponse({'status':'failed','message':'Questions does not exist'})
		data = serializers.serialize('json', ques)
		return JsonResponse(data, safe=False)
	else:
		return JsonResponse({'error':'Only available via GET.','status_code':'400'})

@csrf_exempt
def add_ques(request):
	if request.method == "POST":
		try:
		# if True:
			try:
				subject = request.POST.get('subject')
				question = request.POST.get('question')
				difficulty = request.POST.get('difficulty')
				op1 = request.POST.get('op1')
				op2 = request.POST.get('op2')
				op3 = request.POST.get('op3')
				op4 = request.POST.get('op4')
				correct_ans = request.POST.get('correct_ans')
			except:
				return JsonResponse({'status':'failed', 'message':'Invalid POST data.'})
			try:
			# if True:
				data={
				'subject':subject,
				'difficulty':difficulty,
				'ques':question,
				'op1':op1,
				'op2':op2,
				'op3':op3,
				'op4':op4,
				'correct_ans':correct_ans,
				}
				new_ques = Question(**data)
				new_ques.save()
				return JsonResponse({'status':'success'})
			except:
				return JsonResponse({'status':'failed', 'message':"Couldn't create Question object"})
		except:
			return JsonResponse({'status':'failed','message':'None'})
	else:
		return JsonResponse({'error':'Only available via POST.','status_code':'400'})

@csrf_exempt
def edit_ques(request,id):
	if request.method == "POST":
		try:
			ques = Question.objects.get(id=id)
		except:
			return JsonResponse({'status':'failed','message':'No question with id='+str(id)})
		try:
			# data = request.POST
			querydict = QueryDict('', mutable=True)
			for key in request.POST.iteritems():
			    queslist = ques[key].split(',')
			    querydict.setlist(key, queslist)
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
			Question.objects.filter(id=id).update(**querydict)
			# post.save()
			return HttpResponse(data)
		except Exception as e:
			return HttpResponse(e)
		# except:			
		# 	return JsonResponse({'status':'failed','message':'Cannot update post.'})
	else:
		return JsonResponse({'error':'Only available via PATCH.','status_code':'400'})

@csrf_exempt
# Delete a question
def delete_ques(request,id):
	if request.method == 'DELETE':
		try:
			ques = Question.objects.get(id=id)
		except:
			return JsonResponse({'status':'failed','message':'Question does not exist'})
		try:
			ques.delete()
			return JsonResponse({'status':'success'})
		except:
			return JsonResponse({'status':'failed','message':'Cannot delete question at the moment.'})
	else:
		return JsonResponse({'error':'Only available via DELETE.','status_code':'400'})