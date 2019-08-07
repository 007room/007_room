from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
from main.models import CustomUser


class AuthenticationForm(forms.Form):
    pass


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nickname = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "nickname", "password1", "password2","area","gender","profile_image")

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.nickname = self.cleaned_data["nickname"]
        user.email = self.cleaned_data["email"]
        user.area = self.cleaned_data["area"]
        user.gender = self.cleaned_data["gender"]
        user.profile_image = self.cleaned_data["profile_image"]
        
        if commit:
            user.save()
        return user