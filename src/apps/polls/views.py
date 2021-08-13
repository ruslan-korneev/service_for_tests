from django.shortcuts import render
from django.views.generic.list import ListView
from apps.polls.models import Answer


class PollsList(ListView):
#    reply = 'Polls:'
#    for question in Question.objects.all():
#        reply += f'\n  {question.title}'
#    return HttpResponse(reply)
    model = Answer
