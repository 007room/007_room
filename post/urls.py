from django.urls import path
from .  import views


app_name = 'post'
urlpatterns = [
    path('detail/<int:pk>',views.PostDetailView.as_view(), name = 'detail'),
    path('new', views.PostCreateView.as_view(), name='post_new'),
    path('new_review',views.ReviewCreateView.as_view(), name = 'new_review'),
    path('new_qna',views.QnaCreateView.as_view(), name = 'new_qna'),
   

]