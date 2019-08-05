from django.shortcuts import render

# Create your views here.
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
