from django.urls import path
from .  import views
app_name = 'accounts'

urlpatterns = [
    path('signup/',views.CreateUserView.as_view(), name = 'signup'),
    path('login/done',views.RegisteredView.as_view(), name = 'create_user_done'),
]
