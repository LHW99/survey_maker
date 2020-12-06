from django.urls import path
from . import views
from django.urls import include
from django.views.generic import RedirectView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# home page
urlpatterns = [
  path('', views.index, name='index')
]

# survey display pages
urlpatterns += [
  path('survey/', views.SurveyListView.as_view(), name='survey-list'),
  path('survey/<int:pk>/', views.SurveyDetailView.as_view(), name='survey-detail')
]

# user survey display pages
urlpatterns += [
  path('mysurvey/', views.UserSurvey.as_view(), name='user-survey'),
]

# for log-ins and authentications
urlpatterns += [
  path('accounts/', include('django.contrib.auth.urls'))
]

# for survey editors
urlpatterns += [
  path('survey/create', views.SurveyCreate.as_view(), name='survey-create'),
  path('survey/<int:pk>/update', views.SurveyUpdate.as_view(), name='survey-update'),
  path('survey/<int:pk>/delete', views.SurveyDelete.as_view(), name='survey-delete'),
]

# re questions
urlpatterns += [
  path('survey/<int:pk>/update/question', views.QuestionCreate.as_view(), name='question-create'),
]

# re answers
urlpatterns += [
  path('survey/<int:pk>/update/<int:alt_pk>', views.AnswerCreate.as_view(), name='answer-create'),
]

# submissions
urlpatterns += [
  path('survey/<int:pk>/submit/', views.submit, name='submit')
]

# results
urlpatterns += [
  path('survey/<int:pk>/results', views.SurveyResults.as_view(), name='results'),
]