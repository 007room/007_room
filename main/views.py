from .models import Post, Review
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import DetailView, CreateView
from django.http.response import HttpResponseRedirect
from hitcount.views import HitCountDetailView
from .forms import ReviewForm
# Create your views here.
class PostDetailView(HitCountDetailView):
    model = Post
    count_hit = True
    template_name = 'main/postdetail.html'

    def get_context_data(self, **kwargs):
        ctx =  super(PostDetailView, self).get_context_data(**kwargs)
        ctx['comment_form'] = ReviewForm(initial={'post_pk':self.object.pk})
 
        return ctx

class ReviewCreateView(CreateView):
    model = Review
    template_name = 'main/postdetail.html'

    
    # def dispatch(self, *args, **kwargs):
    #     return super(ReviewCreateView, self).dispatch(*args, **kwargs)

    # def form_valid(self, form):
    #     parent_link = Post.objects.get(pk = form.cleaned_data['post_pk'])
        
    #     new_review = form.save(commit=False)
    #     # new_comment.post = self.request.GET['post_pk']
    #     new_review.post = parent_link
    #     new_review.user = self.request.user

    #     new_review.save()

    #     return HttpResponseRedirect(reverse('main:detail', kwargs={'pk':parent_link.pk}))
    
    # def get_initial(self):
    #     initial_data = super(ReviewCreateView, self).get_initial()
    #     initial_data['post_pk'] = self.request.GET['post_pk']

    def get_context_data(self, **kwargs):
        ctx =  super(ReviewCreateView, self).get_context_data(**kwargs)
        # ctx['comment_form'] = ReviewForm(initial={'post_pk':self.object.pk})
 
        return ctx