from django.shortcuts import render, redirect
# Create your views here.

from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import SearchForm
from .models import Post


class ListView(ListView, FormView):
    template_name = 'main/list.html'
    context_object_name = 'post_list'
    form_class = SearchForm
    model = Post

    def form_valid(self, form): #post method로 값이 전달되면
        word = '%s' %self.request.POST['word'] # 검색어
        post_list = Post.objects.filter(
            Q(title__icontains=word) | Q(context__icontains=word) # Q 객체를 써서 검색한다. title과 content 칼럼에 대소문자 구분 없이 포함 검사( contains)
        ).distinct() # 중복을 제거한다.
        context = {}
        context['object_list'] = post_list # 검색된 결과를 컨텍스트 변수에 담는다
        context['search_word'] = word # 검색어를 컨텍스트 변수에 담는다
        return render(self.request, 'main/list.html', context)

