from django.urls import path
from apps.polls.views import QuestionList


urlpatterns = [
    path('', QuestionList.as_view(), name='questions'),
]
