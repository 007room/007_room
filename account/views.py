from django.conf import settings
from main.models import CustomUser
from django.contrib.auth.models import AbstractUser
from .forms import CreateUserForm, UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView,CreateView
# Create your views here.

class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

class CreateUserView(CreateView): 
    template_name = 'registration/signup.html'
    form_class =  CreateUserForm
    success_url = reverse_lazy('main:list')


class RegisteredView(TemplateView):
    template_name = 'registration/signup_done.html'