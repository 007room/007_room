from django.urls import path
from . import views


app_name = 'guest'
urlpatterns = [
    path('', views.Main.as_view(), name = 'main'),
    path('/list', views.List.as_view(), name = 'list'),

]