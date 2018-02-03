from django.contrib import admin
from .models import Question, Session, Response

# Register your models here.

admin.site.register(Question)
admin.site.register(Session)
admin.site.register(Response)