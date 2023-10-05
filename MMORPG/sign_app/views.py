from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = 'posts/'
    template_name = 'sign/signup.html'
