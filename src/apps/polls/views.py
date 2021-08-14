from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from apps.polls.models import Test

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class CustomLoginView(LoginView):
    template_name = 'polls/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tests')


class RegisterPage(FormView):
    template_name = 'polls/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tests')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tests')
        return super(RegisterPage, self).get(*args, **kwargs)


class TestList(LoginRequiredMixin, ListView):
    model = Test
    context_object_name = 'tests'
    paginate_by = 10
    template_name = 'polls/tests.html'


class TestDetail(LoginRequiredMixin, DetailView):
    model = Test
    context_object_name = 'test'
    template_name = 'polls/test.html'
