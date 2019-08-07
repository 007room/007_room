from main.models import Post, Review, Qna, Review_image
from .forms import ReviewForm, QnaForm, ImageFormSet,PostForm,DateInput
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from hitcount.views import HitCountDetailView
from .forms import ReviewForm, QnaForm, ImageForm, PostForm
from django.forms import modelformset_factory
# taemi

ImageFormSet = modelformset_factory(Review_image, form=ImageForm, extra=1, min_num=1)

# Create your views here.
class PostDetailView(HitCountDetailView):
    model = Post
    count_hit = True
    template_name = 'post/postdetail.html'

    def get_context_data(self, **kwargs):
        ctx =  super(PostDetailView, self).get_context_data(**kwargs)
        ctx['comment_form'] = ReviewForm(initial={'post_pk':self.object.pk})
        ctx['qna_form'] = QnaForm(initial={'post_pk':self.object.pk})
        ctx['image_formset'] = ImageFormSet(queryset=Review_image.objects.none())
    
 
        return ctx
    

class PostCreateView(CreateView):
    model = Post
    template_name = 'post/post_new.html'
    form_class = PostForm

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.user = self.request.user
        new_post.cleaned_data['choose_date'].widget = DateTimePickerInput()
        new_post.save()
        return HttpResponseRedirect(reverse('main:list', ))
        

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post/delete.html'
    success_url = reverse_lazy('main:list')


class ReviewCreateView(CreateView):
    model = Review
    template_name = 'post/postdetail.html'
    form_class = ReviewForm
    
    def dispatch(self, *args, **kwargs):
        return super(ReviewCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        # ImageFormSet = modelformset_factory(Review_image, form=ImageForm, extra=2)
        parent_link = Post.objects.get(pk = form.cleaned_data['post_pk'])
        new_review = form.save(commit=False)
        # new_comment.post = self.request.GET['post_pk']
        new_review.post = parent_link
        new_review.user = self.request.user
        new_review.save()
        image_formset = ImageFormSet(self.request.POST, self.request.FILES,queryset=Review_image.objects.none())
        # print('image_formset',image_formset)
        for form in image_formset:
            if form.is_valid():
                print('에러에러')
            else :
                print(form,'\n')
                image = form.cleaned_data['images']
                photo = Review_image(review=new_review, images=image, user=self.request.user)
                photo.save()
        
        return HttpResponseRedirect(reverse('post:detail', kwargs={'pk':parent_link.pk}))
    
    def get_initial(self):
        initial_data = super(ReviewCreateView, self).get_initial()
        initial_data['post_pk'] = self.request.GET['post_pk']

    def get_context_data(self, **kwargs):
        ctx =  super(ReviewCreateView, self).get_context_data(**kwargs)
        # ctx['comment_form'] = ReviewForm(initial={'post_pk':self.object.pk})
    


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
        return HttpResponseRedirect(reverse('post:detail', kwargs={'pk':parent_link.pk}))


class PostCreateView(CreateView):
    model = Post
    template_name = 'post/post_new.html'
    form_class = PostForm

    def form_valid(self, form):
        
        new_post = form.save(commit=False)
        new_post.user = self.request.user
        new_post.save()
        return HttpResponseRedirect(reverse('main:list', ))
        
