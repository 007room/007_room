
from main.models import *#Post, Review, Qna, Review_image, Comment
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import DetailView, CreateView, DeleteView,UpdateView, ListView, FormView
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, HttpResponse
from hitcount.views import HitCountDetailView
from django.forms import modelformset_factory
from bootstrap_datepicker_plus import DateTimePickerInput

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

    def get_form(self):
        form = super().get_form()
        form.fields['start_datetime'].widget = MyDatePickerInput()
        form.fields['end_datetime'].widget = MyDatePickerInput()
        return form

    def form_valid(self, form):       
        new_post = form.save(commit=False)
        new_post.user = self.request.user
        new_post.save()

        return HttpResponseRedirect(reverse('main:list', kwargs={'pk':parent_link.pk}))


class PostUpdateView(UpdateView): 
    model = Post
    template_name = 'post/update.html'
    form_class = PostForm
    success_url = reverse_lazy('main:list')
    
    def get_form(self):
        form = super().get_form()
        form.fields['start_datetime'].widget = MyDatePickerInput()
        form.fields['end_datetime'].widget = MyDatePickerInput()
        return form

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
        return ctx

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
        return HttpResponseRedirect(reverse('post:detail_qna', kwargs={'pk':parent_link.pk}))

class CommentCreateView(ReviewCreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        parent_link = Post.objects.get(pk = form.cleaned_data['post_pk'])
        new_comment = form.save(commit=False)
        new_comment.post = parent_link
        new_comment.qna = Qna.objects.get(pk = self.request.GET['qna_pk'])
        new_comment.save()
        return HttpResponseRedirect(reverse('post:detail_qna', kwargs={'pk':parent_link.pk}))


        
class QnaDetailView(ListView):
    model = Qna
    template_name = 'post/qna.html'

    def get_context_data(self, **kwargs):
        ctx =  super(QnaDetailView, self).get_context_data(**kwargs)
        ctx['qna_form'] = QnaForm(initial={'post_pk':self.kwargs['pk']})
        ctx['comment_form'] = CommentForm(initial={'post_pk':self.kwargs['pk']})
        return ctx
    
    def get_queryset(self):
        return Qna.objects.filter(post=self.kwargs['pk'])

class ReviewDetailView(ListView):
    model = Review
    template_name = 'post/review.html'

    def get_context_data(self, **kwargs):
        ctx =  super(ReviewDetailView, self).get_context_data(**kwargs)
        ctx['comment_form'] = ReviewForm(initial={'post_pk':self.kwargs['pk']})
        ctx['image_formset'] = ImageFormSet(queryset=Review_image.objects.none())
        ctx['confirm_form'] = ConfirmForm()
        ctx['post_pk'] = self.kwargs['pk']
        return ctx
    def get_queryset(self):
        return Review.objects.filter(post=self.kwargs['pk'])

def confirm_review(request):
    review = Review.objects.get(pk = request.GET['review_pk'])
    review.confirm = True
    review.save()
    return HttpResponseRedirect(reverse('post:detail_review', kwargs={'pk':request.GET['post_pk']}))


class ReportView(FormView):
    template_name = 'post/report.html'
    form_class = ReportForm
    ordering = ['-created_date']     
    model = CustomUser      

    def form_valid(self, form): #post method로 값이 전달되면
        new_report = form.save(commit=False)
        new_report.reporter_user = self.request.user
        user = CustomUser.objects.filter(email = new_report.reported_user)
        context = {}
        context['user'] = user
        new_report.save()
        # return HttpResponseRedirect(reverse('post:report_done_check', ))
        return render(self.request, 'post/report_done.html', context )   
        
# def ReportDoneCheck(request):
#     return render(request, 'post/report_done.html')

def ReportDone(request):
    return HttpResponse('<script type="text/javascript">window.close()</script>') 

