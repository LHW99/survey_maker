from django.db import models
from django.urls import reverse # Used to generate URLs by reversing URL patterns
import uuid # required for unique instances
from django.contrib.auth.models import User # lets us use user
from datetime import date

# Create your models here.
class Answer(models.Model):
  selection = models.CharField(max_length=200)
  query = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True)

  def __str__(self):
    return self.answer

class Question(models.Model):
  query = models.CharField(max_length=300)
  survey = models.ForeignKey('Survey', on_delete=models.SET_NULL, null=True)

  def __str__(self):
    return self.query

class Survey(models.Model):
  title = models.CharField(max_length=300, blank=False)
  surveyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, unique=False)

  def __str__(self):
    return self.title