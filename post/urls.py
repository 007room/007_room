from django.urls import path
from .  import views


app_name = 'post'
urlpatterns = [
    #post
    path('detail/<int:pk>',views.PostDetailView.as_view(), name = 'detail'),
    path('new', views.PostCreateView.as_view(), name='new'),
    path('edit/<int:pk>', views.PostUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>',views.PostDeleteView.as_view(), name = 'delete'),
    #review
    path('new_review',views.ReviewCreateView.as_view(), name = 'new_review'),
    path('review/<int:pk>',views.ReviewDetailView.as_view(), name = 'detail_review'),
    path('confirm',views.confirm_review, name = 'confirm_review'),

    #qna
    path('new_qna',views.QnaCreateView.as_view(), name = 'new_qna'),
    path('qna/<int:pk>',views.QnaDetailView.as_view(), name = 'detail_qna'),
    path('comment/',views.CommentCreateView.as_view(), name = 'new_comment'),
   
    path('detail/<int:pk>/report', views.ReportView.as_view(), name = 'report'),

]