from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
	subject = models.CharField(max_length=15)
	difficulty = models.CharField(max_length=6) # Can be ['Easy', 'Medium', 'Hard'].
	ques = models.TextField()
	op1 = models.TextField()
	op2 = models.TextField()
	op3 = models.TextField()
	op4 = models.TextField()
	correct_ans = models.CharField(max_length=1)

	def __str__(self):
		return str(self.subject) + " " + str(self.id)


class Session(models.Model):
	student = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	start_time = models.DateTimeField(default=timezone.now)
	end_time = models.DateTimeField(blank=True, null=True)
	score = models.IntegerField(default=0)

	def end_test(self):
		self.end_time = timezone.now()
		self.save()

	def __str__(self):
		return self.id

class Response(models.Model):
	question_id = models.IntegerField(default=0)
	response = models.CharField(max_length=1)
	correct_resp = models.CharField(max_length=1)
	sess = models.ForeignKey('Session',on_delete=models.CASCADE)

	def __str__(self):
		return self.question_id