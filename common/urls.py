from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='common/login.html') ,name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('signup/' , views.signup,name='signup'),
    path('profile/<int:user_id>/',views.profile,name='profile'),
    path('profile/<int:user_id>/userinfo/',views.userinfo,name='userinfo'),
    path('profile/<int:user_id>/dropout/',views.dropout,name='dropout'),
    path('profile/<int:user_id>/passwordchange/',views.passwordchange,name='passwordchange'),
]

#재네릭 뷰 방식 - 함수를 직접 정의할 필요가 없음