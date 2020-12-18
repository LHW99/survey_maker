
from django.forms.models import inlineformset_factory
from django.forms import ModelForm
from django import forms
from .models import Survey, Question, Answer

QuestionFormset = inlineformset_factory(Survey, Question, fields=('query',), extra=1)
AnswerFormset = inlineformset_factory(Question, Answer, fields=('selection',), extra=4)

class SurveyForm(forms.ModelForm):
  class Meta: 
    model = Survey
    fields = ['title',]

class QuestionForm(forms.ModelForm):
  class Meta: 
    model = Question
    fields = ['query',]

class AnswerForm(forms.ModelForm):
  class Meta:
    model = Answer
    fields = ['selection',]

class SubmitForm(forms.Form):
  def __init__(self, *args, **kwargs):
    answers = kwargs.pop('answers')
    choices = {(a.pk, a.selection) for a in answers}
    labels = {a.query for a in answers}
    super().__init__(*args, **kwargs)
    answer_field = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, required=True)
    self.fields['answer'] = answer_field
    self.fields['answer'].label = labels

class BaseSubmitFormSet(forms.BaseFormSet):
  def get_form_kwargs(self, index):
    kwargs = super().get_form_kwargs(index)
    kwargs['answers'] = kwargs['answers'][index]
    return kwargs
  