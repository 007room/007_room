from django.shortcuts import render

# Create your views here.

from django.views.generic.list import ListView

from .models import Post


class ListView(ListView):
    template_name = 'main/list.html'
    context_object_name = 'post_list'
    model = Post