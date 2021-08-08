import os

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate ,login
from django.contrib.auth.models import User
from .forms import UserForm, ProfileForm
from .models import Profile


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
    profile_form = user.profile
    context = {'question_list':question_list , 'answer_list':answer_list ,'user_id':user_id , 'profile_form' :profile_form}
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
    context = {'form' : profile_form}
    return render(request,'common/userinfo.html',context)