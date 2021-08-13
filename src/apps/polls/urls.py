from django.urls import path
from apps.polls.views import PollsList


urlpatterns = [
    path('', PollsList.as_view(), name='polls'),
]
