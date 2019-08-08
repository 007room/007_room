from django.urls import path
from .  import views


app_name = 'post'
urlpatterns = [
    #post
    path('detail/<int:pk>',views.PostDetailView.as_view(), name = 'detail'),
    path('new', views.PostCreateView.as_view(), name='post_new'),
    path('edit/<int:pk>', views.PostUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>',views.PostDeleteView.as_view(), name = 'delete'),
    #review
    path('new_review',views.ReviewCreateView.as_view(), name = 'new_review'),

    #qna
    path('new_qna',views.QnaCreateView.as_view(), name = 'new_qna'),
    path('detail/<int:pk>/report', views.ReportView.as_view(), name = 'report'),

]