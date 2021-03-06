from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms

from common.models import Profile, myUser


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    class Meta:
        model = myUser
        fields =("username","email")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname','photo']
        labels = {
            'nickname':'닉네임',
            'photo':'이미지'
        }