from .models import Post, Review, Qna, Review_image
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import DetailView, CreateView
from django.http.response import HttpResponseRedirect
from hitcount.views import HitCountDetailView
from .forms import ReviewForm, QnaForm, ImageFormSet
# taemi
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.db.models import Q
from .forms import SearchForm
from .models import Post

# Create your views here.
class PostDetailView(HitCountDetailView):
    model = Post
    count_hit = True
    template_name = 'main/postdetail.html'

    def get_context_data(self, **kwargs):
        ctx =  super(PostDetailView, self).get_context_data(**kwargs)
        ctx['comment_form'] = ReviewForm(initial={'post_pk':self.object.pk})
        ctx['qna_form'] = QnaForm(initial={'post_pk':self.object.pk})
        ctx['image_formset'] = ImageFormSet()
 
        return ctx

class ReviewCreateView(CreateView):
    model = Review
    template_name = 'main/postdetail.html'
    form_class = ReviewForm
    
    def dispatch(self, *args, **kwargs):
        return super(ReviewCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        parent_link = Post.objects.get(pk = form.cleaned_data['post_pk'])
        new_review = form.save(commit=False)
        # new_comment.post = self.request.GET['post_pk']
        new_review.post = parent_link
        new_review.user = self.request.user

        new_review.save()
        
        image_formset = ImageFormSet(self.POST, self.FILES)
        for form in image_formset.cleaned_data:
            image = form['images']
            photo = Review_image(review=new_review, images=image)
            photo.save()

        return HttpResponseRedirect(reverse('main:detail', kwargs={'pk':parent_link.pk}))
    
    def get_initial(self):
        initial_data = super(ReviewCreateView, self).get_initial()
        initial_data['post_pk'] = self.request.GET['post_pk']

    def get_context_data(self, **kwargs):
        ctx =  super(ReviewCreateView, self).get_context_data(**kwargs)
        # ctx['comment_form'] = ReviewForm(initial={'post_pk':self.object.pk})
 
    #     return ctx

class QnaCreateView(ReviewCreateView):
    model = Qna
    form_class = QnaForm


    def form_valid(self, form):
        parent_link = Post.objects.get(pk = form.cleaned_data['post_pk'])
        
        new_qna = form.save(commit=False)
        # new_comment.post = self.request.GET['post_pk']
        new_qna.post = parent_link
        new_qna.user = self.request.user
        

        new_qna.save()

        return HttpResponseRedirect(reverse('main:detail', kwargs={'pk':parent_link.pk}))

      
      #taemi
      
class ListView(ListView):
    template_name = 'main/list.html'
    context_object_name = 'post_list'
    model = Post



# 검색 
class SearchFormView(FormView):
    form_class = SearchForm
    template_name= 'main/list.html'
    
    def form_valid(self, form): #post method로 값이 전달되면
        form_class = SearchForm # 정의 안 해주면 오류
        word = '%s' %self.request.POST['word'] # 검색어
        post_list = Post.objects.filter(
            Q(title__icontains=word) | Q(context__icontains=word) # Q 객체를 써서 검색한다. title과 content 칼럼에 대소문자 구분 없이 포함 검사( contains)
        ).distinct() # 중복을 제거한다.
        context = {}
        context['object_list'] = post_list # 검색된 결과를 컨텍스트 변수에 담는다
        context['search_word'] = word # 검색어를 컨텍스트 변수에 담는다
        context['form'] = form_class
        return render(self.request, 'main/list.html', context)
#create
def post_new(request):
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            # post.Modified_date = request.META['Modified_date']
            post.save()
            return redirect('post:IndexView')
    else:
        form = PostForm()
    return render(request, 'post/post_new.html',{'form':form,})
