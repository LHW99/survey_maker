import datetime
import re

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views import generic, View
from surveyer.models import Answer, Question, Survey
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .forms import QuestionFormset, AnswerFormset, SurveyForm, QuestionForm, AnswerForm, SubmitForm, BaseSubmitFormSet
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory

# Create your views here.

def index(request):
  return render(request, 'index.html')

class SurveyListView(generic.ListView):
  model = Survey
  paginate_by = 10

class SurveyDetailView(generic.DetailView):
  model = Survey

class UserSurvey(LoginRequiredMixin, generic.ListView):
  model = Survey
  template_name = 'surveyer/user_survey_list.html'
  paginate_by = 10

  def get_queryset(self):
    return Survey.objects.filter(surveyer=self.request.user)

class SurveyCreate(LoginRequiredMixin, CreateView):
  model = Survey
  fields = ['title',]
  template_name = 'survey_form.html'
  success_url = 'survey-update'

  def post(self, request):
    form = SurveyForm(request.POST)
    if form.is_valid():
      survey = form.save(commit=False)
      survey.surveyer = self.request.user
      survey.save()
      return redirect('survey-update', pk=survey.id)
    else:
      form = SurveyForm()
    return render(request, 'survey_form.html', {'form': form})

class SurveyUpdate(LoginRequiredMixin, UpdateView):
  model = Survey
  fields = ['title',]
  template_name = 'survey_update.html'

class QuestionCreate(LoginRequiredMixin, CreateView):
  model = Question
  fields = ['query',]
  success_url = reverse_lazy('survey-update')

  def post(self, request, pk):
    form = QuestionForm(request.POST)
    if form.is_valid():
      question = form.save(commit=False)
      form.instance.survey_id = self.kwargs.get('pk')
      question.save()
      return redirect('survey-update', pk=pk)
    else:
      form = QuestionForm()
    return render(request, 'question_form.html', {'form': form})

class AnswerCreate(LoginRequiredMixin, CreateView):
  model = Answer
  fields = ['selection',]
  success_url = reverse_lazy('survey-update')

  def post (self, request, pk, alt_pk):
    form = AnswerForm(request.POST)
    if form.is_valid():
      answer = form.save(commit=False)
      form.instance.query_id = self.kwargs['alt_pk']
      answer.save()
      return redirect('survey-update', pk=pk)
    else:
      form = AnswerForm()
    return render(request, 'answer_form.html', {'form':form})

class SurveyDelete(LoginRequiredMixin, DeleteView):
  model = Survey
  success_url = reverse_lazy('user-survey')

class SurveyResults(LoginRequiredMixin, generic.DetailView):
  model = Survey
  template_name = 'results.html'

def submit(request, pk):
  survey = Survey.objects.prefetch_related('question_set__answer_set').get(pk=pk)
  questions = survey.question_set.all()
  answers = [q.answer_set.all() for q in questions]
  form_kwargs = {'empty_permitted': False, 'answers': answers}
  #SubmitFormSet = formset_factory(SubmitForm, extra=len(questions), formset=BaseSubmitFormSet)
  SubmitFormSet = inlineformset_factory(Question, Answer, extra=len(questions), exclude=['question',])
  if request.method == 'POST':
    #formset = SubmitFormSet(request.POST, form_kwargs=form_kwargs)
    formset = SubmitFormSet(request.POST, instance=question)
    if formset.is_valid():
      #for form in formset:
      option = formset.get(pk=request.POST['answers'])
      option.vote += 1
      option.save()
      #return HttpResponse(selection)
      return redirect('results', pk=survey_pk)
  
  else:
    formset = SubmitFormSet(form_kwargs=form_kwargs)
  
  return render(request, 'surveyer/submit.html', {'survey': survey, 'formset': formset,})
