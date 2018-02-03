from django.shortcuts import render
from django.http import QueryDict,HttpResponse
from django.core import serializers
from django.http import JsonResponse
from .models import Question, Session, Response
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

import json


# Global Point Scale
diff = {
	'High' : 3,
	'Medium' : 2,
	'Low' : 1
}

av_score = 10


@csrf_exempt
def starttest(request):
	if request.method == "POST":
		try:
		# if True:
			try:
				student = request.POST.get('student')
				subject = request.POST.get('subject')
			except:
				return JsonResponse({'status':'failed', 'message':'Invalid POST data.'})
			try:
				user = User.objects.get(username=student)
			except:
				return JsonResponse({'status':'failed','message':'User '+student+' does not exist.'})
			try:
				s_data = {
				'student':user,
				}
				sess = Session(**s_data)
				sess.save()
			except:
				return JsonResponse({'status':'failed','message':'Cannot create Session object'})
			try:
				questions = Question.objects.filter(subject=subject)
				if len(questions) == 0:
					return JsonResponse({'status':'failed','message':'No questions in this category.'})
			except:
				return JsonResponse({'error':'Not Found','status_code':'404'})
			
			data = serializers.serialize('json', questions)
			data = data.replace(', \"correct_ans\": \"A\"',"")
			data = data.replace(', \"correct_ans\": \"B\"',"")
			data = data.replace(', \"correct_ans\": \"C\"',"")
			data = data.replace(', \"correct_ans\": \"D\"',"")
			to_send = {
			'sess_id':sess.id,
			'questions':data
			}
			return JsonResponse(to_send, safe=False)
		
		except:
			return JsonResponse({'status':'failed','message':'none'})

	else:
		return JsonResponse({'error':'Only available via POST.','status_code':'400'})


@csrf_exempt
def stoptest(request):
	if request.method == "POST":
		try:
		# if True:
			try:
				sess_id = request.POST.get('sess_id')
				resp = request.POST.get('responses') # {question_id:response}
				pos = resp.rfind(',')
				if pos > resp.rfind(':'):
					resp = resp[:pos] + resp[pos + 1:]
				resp = resp.replace("'", "\"")
				resp = json.loads(resp)
			except:
				return JsonResponse({'status':'failed', 'message':'Invalid POST data.'})
			try:
				sess = Session.objects.get(id=sess_id)
			except:
				return JsonResponse({'status':'failed','message':'Session does not exist.'})
			try:
			# if True:
				score = 0
				for key in resp:
					try:
						ques = Question.objects.get(id=int(key))
					except:
						pass
					else:
						r_data={
						'question_id':ques.id,
						'response':resp[key],
						'correct_resp':ques.correct_ans,
						'sess':sess
						}
						res = Response(**r_data)
						res.save()
						
						global diff, av_score
						if ques.correct_ans == resp[key]:
							score += diff[ques.difficulty] * av_score

				sess.score = score
				sess.end_test()
			except:
				return JsonResponse({'status':'failed','message':'Cannot update Session object'})

			data = serializers.serialize('json', [sess])
			return JsonResponse(data, safe=False)

		except:
			return JsonResponse({'status':'failed','message':'none'})

	else:
		return JsonResponse({'error':'Only available via POST.','status_code':'400'})


def ques_all(request):
	if request.method == "GET":
		try:
			ques = Question.objects.all()
		except:
			return JsonResponse({'status':'failed','message':'Questions does not exist'})
		data = serializers.serialize('json', ques)
		data = data.replace(', \"correct_ans\": \"A\"',"")
		data = data.replace(', \"correct_ans\": \"B\"',"")
		data = data.replace(', \"correct_ans\": \"C\"',"")
		data = data.replace(', \"correct_ans\": \"D\"',"")
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
			p_data = request.POST.dict()
			for attr, value in p_data.items():
				setattr(ques, attr, value)
			ques.save()
			return JsonResponse({'status':'success'})
		except:
			return JsonResponse({'status':'failed', 'message':'Cannot update Question Object.'})
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


def revise(request,sess_id):
	if request.method == 'GET':
		try:
		# if True:
			s = Session.objects.get(id=sess_id)
			resp = Response.objects.filter(sess=s)
			if len(resp) == 0:
				return JsonResponse({'status':'failed','message':'No responses with this Session ID'})
		except:
			return JsonResponse({'status':'failed','message':'Cannot find Reponse/Session Object'})

		to_send={}
		for r in resp:
			try:
				ques = Question.objects.get(id=r.question_id)
			except:
				pass
			else:
				q = {
				'student_response':r.response,
				'correct_response':r.correct_resp
				}
				to_send[ques.ques] = q
		# data = serializers.serialize('json', resp)
		return JsonResponse(to_send, safe=False)
	else:
		return JsonResponse({'error':'Only available via GET.','status_code':'400'})
