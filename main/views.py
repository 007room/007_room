from django.shortcuts import render, redirect, reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.db.models import Q
from .forms import SearchForm
from .models import Post
import operator


class List(ListView):
    template_name = 'main/list.html'
    context_object_name = 'object_list'
    model = Post
    ordering = ['-created_date']           # 기본 값
    paginate_by = 2  # Display 10 objects per page


# 페이지네이션
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

        if sort == 'new' :
            print('들어옴')
            # self.ordering = ['created_date']
            posts = Post.objects.order_by('-created_date')
            context['object_list'] = posts[current_page*2-2: current_page*2]
        elif sort == 'likes':
            # 좋아요 정렬
            pass
        elif sort == 'review':
            order = {}
            posts = Post.objects.all()
            for post in posts :
                order[post] = post.reviews.count
            data = sorted(order.items(), key=operator.itemgetter(1))
            context['object_list'] = data[current_page*2-2: current_page*2]
            
            # sorted(order, key=lambda k : order[k], reverse=True)
            # res = sorted(order.items(), key=(lambda x: x[1]), reverse = True)
            # context['object_list'] = res[current_page*2-2: current_page*2]
            # context['object_list'] = posts[current_page*2-2: current_page*2]
            pass
        elif sort == 'price_up':
            # 가격(오름차순)
            pass
        elif sort == 'price_down':
            # 가격(내림차순)
            pass

        return context

class SearchView(FormView):
    template_name = 'main/search.html'
    form_class = SearchForm
    ordering = ['-created_date']           # 기본 값

    # 검색
    def form_valid(self, form): #post method로 값이 전달되면
        form_class = SearchForm # 정의 안 해주면 오류
        word = '%s' %self.request.POST['word'] # 검색어
        post_list = Post.objects.filter(
            Q(title__icontains=word) | Q(context__icontains=word) # Q 객체를 써서 검색한다. title과 content 칼럼에 대소문자 구분 없이 포함 검사( contains)
        ).distinct() # 중복을 제거한다.
        context = {}
        # context = super(ListView, self).form_valid(form)
        context['object_list'] = post_list # 검색된 결과를 컨텍스트 변수에 담는다
        context['search_word'] = word # 검색어를 컨텍스트 변수에 담는다
        context['form'] = form_class
        return render(self.request, self.template_name , context)
       

