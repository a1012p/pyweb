from django.shortcuts import render , redirect
from django.contrib.auth import authenticate ,login
from django.contrib.auth.models import User
from .forms import UserForm

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username= username , password=raw_password)
            login(request,user)
            return redirect('index')
    else:
        form = UserForm()
    context = {'form' : form}
    return render(request,'common/signup.html',context)

def userinfo(request,user_id):
    user = User.objects.get(id=user_id)
    question_list = user.author_question.all().order_by('-create_date')
    answer_list = user.author_answer.all().order_by('-create_date')
    context = {'question_list':question_list , 'answer_list':answer_list ,'user_id':user_id}
    return render(request,'common/userinfo.html',context)