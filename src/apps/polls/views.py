from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from apps.polls.models import Question

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class CustomLoginView(LoginView):
    template_name = 'polls/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('questions')


class RegisterPage(FormView):
    template_name = 'polls/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('questions')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('questions')
        return super(RegisterPage, self).get(*args, **kwargs)


class QuestionList(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = 'questions'
