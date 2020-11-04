import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from surveyer.models import Answer, Question, Survey
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
#from .forms import QuestionFormset, AnswerFormset, SurveyForm, QuestionForm, AnswerForm

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
  fields = ['name',]
  template_name = 'survey_form.html'

  def post(self, request):
    form = SurveyForm(request.POST)
    if form.is_valid():
      survey = form.save(commit=False)
      survey.surveryer = request.user
      return redirect('survey-create2', pk=survey.id)
    else:
      form = SurveyForm()
    return render(request, 'survey_form.html', {'form': form})

class SurveyCreate2(LoginRequiredMixin, UpdateView):
  model = Question
  fields = ('question',)
  template_name = 'survey_form2.html'

  def get_context_data(self, *args, **kwargs):
    data = super().get_context_data(**kwargs)
    if self.request.POST:
      data['answer'] = AnswerFormset(self.request.POST)
    else:
      data['answer'] = AnswerFormset()
    return data
  
  def form_valid(self, form):
    context = self.get_context_data()
    answer = context['answer']
    self.object = form.save()
    if answer.is_valid():
      answer.instance = self.object
      answer.save()
    return super().form_valid(form)

class SurveyUpdate(LoginRequiredMixin, UpdateView):
  model = Survey
  fields = ('name',)
  template_name = 'survey_update.html'

class SurveyDelete(LoginRequiredMixin, DeleteView):
  model = Survey
  success_url = reverse_lazy('user-survey')