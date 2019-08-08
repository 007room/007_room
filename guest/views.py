from django.shortcuts import render, redirect, reverse
from django.views.generic.list import ListView
from main.models import Post


# Create your views here.

class Main(ListView):
    template_name = 'guest/main.html'
    model = Post
    

class List(ListView):
    template_name = 'guest/buy_list.html'
    context_object_name = 'object_list'
    model = Post
    ordering = ['-created_date']           # 기본 값
    paginate_by = 2  # Display 10 objects per page

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        sort = self.request.GET.get('sort','')
        context['sort'] = sort
        paginator = context['paginator']
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
# 여기서부터 fitler로 내가 쓴 글만 보기
        user = self.request.user
        posts = Post.objects.filter(user_id = user).order_by('-created_date')
        context['object_list'] = posts[current_page*2-2: current_page*2]
        return context