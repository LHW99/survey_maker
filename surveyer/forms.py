
from django.forms.models import inlineformset_factory
from django.forms import ModelForm
from django import forms
from .models import Survey, Question, Answer

QuestionFormset = inlineformset_factory(Survey, Question, fields=('query',), extra=3)
AnswerFormset = inlineformset_factory(Question, Answer, fields=('selection',), extra=4)

class SurveyForm(ModelForm):
  class Meta: 
    model = Survey
    fields = ['title',]

class QuestionForm(ModelForm):
  class Meta: 
    model = Question
    fields = ['query',]

class AnswerForm(ModelForm):
  class Meta:
    model = Answer
    fields = '__all__'