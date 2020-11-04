from django.contrib import admin
from .models import Question, Answer, Survey

# Register your models here.

class AnswerInline(admin.TabularInline):
  model = Answer

class QuestionAdmin(admin.ModelAdmin):
  inlines = [
    AnswerInline,
  ]

class QuestionInline(admin.TabularInline):
  model = Question

class SurveyAdmin(admin.ModelAdmin):
  inlines = [
    QuestionInline,
  ]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Survey, SurveyAdmin)