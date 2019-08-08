from django.urls import path
from . import views


app_name = 'main'
urlpatterns = [
    path('', views.List.as_view(), name = 'list'),
    # path('search/', views.SearchFormView.as_view(), name= 'search'),
    path('search/', views.SearchView.as_view(), name = 'search'),
    path('sort/', views.ListView.as_view(), name = 'sort'),
    path('myaccount/', views.AccountView.as_view(), name = 'myaccount'),
]