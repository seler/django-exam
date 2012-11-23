from django.contrib import admin

from .models import Question, Answer, Participant

admin.site.register((Question, Answer, Participant))
