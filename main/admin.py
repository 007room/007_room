from django.contrib import admin

from .models import CustomUser, Post, Review, Qna, Application, Qna_image, Post_image, Date, Post_like, Review_like, Comment, Review_image, Report
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.admin import UserAdmin
from account.forms import CreateUserForm, UserChangeForm

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CreateUserForm
    form = UserChangeForm
    model = CustomUser
    list_display = ["username", "email", "nickname","area","gender","profile_image"]



admin.site.register(Post)
admin.site.register(Review)
admin.site.register(Qna)
admin.site.register(Application)
admin.site.register(Qna_image)
admin.site.register(Post_image)
admin.site.register(Date)
admin.site.register(Post_like)
admin.site.register(Review_like)
admin.site.register(Comment)
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Review_image)
admin.site.register(Report)

