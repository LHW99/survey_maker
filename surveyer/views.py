import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect 
from django.views import generic
from surveyer.models import Answer, Question, Survey
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .forms import QuestionFormset, AnswerFormset, SurveyForm, QuestionForm, AnswerForm

# Create your views here.

def index(request):
  return render(request, 'index.html')

class SurveyListView(generic.ListView):
  model = Survey
  paginate_by = 10

class SurveyDetailView(generic.DetailView):
  model = Survey

class QuestionView(generic.View):
  model = Question

class UserSurvey(LoginRequiredMixin, generic.ListView):
  model = Survey
  template_name = 'catalog/user_survey_list.html'
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

  def post (self, request, pk):
    form = AnswerForm(request.POST)
    if form.is_valid():
      answer = form.save(commit=False)
      form.instance.question_id = self.kwargs.get('alt_pk')
      answer.save()
      return redirect('survey-update', pk=pk)
    else:
      form = AnswerForm()
    return render(request, 'answer_form.html', {'form':form})

class SurveyDelete(LoginRequiredMixin, DeleteView):
  model = Survey
  success_url = reverse_lazy('user-survey')