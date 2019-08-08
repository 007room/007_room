from django.urls import path
from . import views


app_name = 'host'
urlpatterns = [
    path('write_list/', views.WriteList.as_view(), name = 'write_list'),
]