import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import check_password, is_password_usable
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .forms import UserForm, ProfileForm
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        Proform = ProfileForm(request.POST,request.FILES)
        if form.is_valid() and Proform.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username= username , password=raw_password)
            profile = Proform.save(commit=False)
            profile.user = user;
            if request.FILES:
                profile.photo = request.FILES['photo']
            profile.nickname = request.POST['nickname']
            profile.save()
            login(request,user)
            return redirect('index')
    else:
        form = UserForm()
        Proform = ProfileForm()
    context = {'form' : form , 'Proform':Proform}
    return render(request,'common/signup.html',context)

def profile(request,user_id):
    user = User.objects.get(id=user_id)
    question_list = user.author_question.all().order_by('-create_date')
    answer_list = user.author_answer.all().order_by('-create_date')
    context = {'question_list':question_list , 'answer_list':answer_list , 'profile' :user.profile}
    return render(request,'common/profile.html',context)

def userinfo(request,user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        profile_form = ProfileForm(request.POST)
        if request.FILES:
            if user.profile.photo:
                os.remove(os.path.join(settings.MEDIA_ROOT, user.profile.photo.path))
            user.profile.photo = request.FILES['photo']
            user.profile.save()
        if profile_form.is_valid():
            myprofile = profile_form.save(commit=False)
            user.profile.nickname = myprofile.nickname
            messages.add_message(request,messages.SUCCESS,"닉네임이 수정되었습니다")
            user.profile.save()
            return redirect('common:userinfo',user_id)
    else:
        profile_form = ProfileForm(instance=user.profile)
    context = {'form' : profile_form ,'profile':user.profile }
    return render(request,'common/userinfo.html',context)

def dropout(request,user_id):
    user = User.objects.get(id=user_id)
    if request.user.is_authenticated:
        logout(request)
    user.profile.delete()
    user.delete()
    return redirect('index')

def passwordchange(request,user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        now_password = request.POST['now_password']
        if check_password(now_password,user.password):
            new_password = request.POST['password1']
            confirm_password = request.POST['password2']
            try:
                validate_password(new_password)
                validate_password(confirm_password)
            except ValidationError as e:
                context = {'profile': user.profile ,'errors':e}
                return render(request,'common/passwordchange.html',context)
            if new_password == confirm_password:
                user.set_password(new_password)
                update_session_auth_hash(request,user)
                user.save()
                messages.success(request,"비밀번호가 정상적으로 변경되었습니다")
                return redirect('common:passwordchange',user_id)
            else:
                messages.warning(request,"새로운 비밀번호를 확인해주세요")
        else:
            messages.warning(request, "현재 비밀번호를 확인해주세요")

    context = {'profile': user.profile}
    return render(request,'common/passwordchange.html',context)
