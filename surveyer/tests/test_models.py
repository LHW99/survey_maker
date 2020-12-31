from django.test import TestCase
from django.urls import reverse

from .models import Question, Answer, Survey

class SurveyModelTests(TestCase):
  def no_user_surveys(self):
    #displays correct message if user has no surveys
    response = self.client.get(reverse('user-survey'))
    self.assertContains(response, 'You have no surveys.')

