from main.models import Post, Review, Qna, Review_image
from .forms import ReviewForm, QnaForm, ImageFormSet,PostForm
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from hitcount.views import HitCountDetailView



# Create your views here.
class PostDetailView(HitCountDetailView):
    model = Post
    count_hit = True
    template_name = 'post/postdetail.html'

    def get_context_data(self, **kwargs):
        ctx =  super(PostDetailView, self).get_context_data(**kwargs)
        ctx['comment_form'] = ReviewForm(initial={'post_pk':self.object.pk})
        ctx['qna_form'] = QnaForm(initial={'post_pk':self.object.pk})
        ctx['image_formset'] = ImageFormSet()
 
        return ctx

class PostCreateView(CreateView):
    model = Post
    template_name = 'post/post_new.html'
    form_class = PostForm

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.user = self.request.user
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

        return HttpResponseRedirect(reverse('post:detail', kwargs={'pk':parent_link.pk}))
    
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
        return HttpResponseRedirect(reverse('post:detail', kwargs={'pk':parent_link.pk}))

<<<<<<< HEAD

=======
      

class PostCreateView(CreateView):
    model = Post
    template_name = 'post/post_new.html'
    form_class = PostForm

    def form_valid(self, form):
        
        new_post = form.save(commit=False)
        new_post.user = self.request.user
        new_post.save()
        return HttpResponseRedirect(reverse('main:list', ))
        
>>>>>>> ff4caf512cd0843ee14499efda0ee0aa3a11039d
