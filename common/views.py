import os

from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, is_password_usable
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .tokens import account_activation_token

from .forms import UserForm, ProfileForm
from .models import Profile, myUser

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        Proform = ProfileForm(request.POST,request.FILES)
        if form.is_valid() and Proform.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username= username , password=raw_password)
            user.active = False;
            user.save()
            profile = Proform.save(commit=False)
            profile.user = user;
            if request.FILES:
                profile.photo = request.FILES['photo']
            profile.nickname = request.POST['nickname']
            profile.save()
            current_site = get_current_site(request)
            message = render_to_string('common/activation_email.html',{
                'user': user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = "회원가입 인증 메일입니다."
            user_email = user.email;
            email = EmailMessage(mail_subject,message,to=[user_email])
            email.send()
            return HttpResponse(
                '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
                'justify-content: center; align-items: center;">'
                '입력하신 이메일<span>로 인증링크가 전송되었습니다.</span>'
                '</div>'
            )
    else:
        form = UserForm()
        Proform = ProfileForm()
    context = {'form' : form , 'Proform':Proform}
    return render(request,'common/signup.html',context)

@login_required(login_url='common:login')
def profile(request,user_id):
    user = myUser.objects.get(id=user_id)
    question_list = user.author_question.all().order_by('-create_date')
    answer_list = user.author_answer.all().order_by('-create_date')
    context = {'question_list':question_list , 'answer_list':answer_list , 'profile' :user.profile}
    return render(request,'common/profile.html',context)

@login_required(login_url='common:login')
def userinfo(request,user_id):
    user = myUser.objects.get(id=user_id)
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

@login_required(login_url='common:login')
def dropout(request,user_id):
    user = myUser.objects.get(id=user_id)
    if request.user.is_authenticated:
        logout(request)
    user.profile.delete()
    user.delete()
    return redirect('index')

@login_required(login_url='common:login')
def passwordchange(request,user_id):
    user = myUser.objects.get(id=user_id)
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

def activate(request,uid64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        user = myUser.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,myUser.DoseNotExsit):
        user = None;
    if user is not None and account_activation_token.check_token(user,token):
        user.active = True
        user.save()
        auth.login(request,user)
        return redirect("index")
    else:
        return render(request,'index')