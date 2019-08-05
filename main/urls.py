from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.ListView.as_view(), name = 'list'),
    # path('search/', views.SearchFormView.as_view(), name= 'search'),

]