from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from accounts.forms import LoginForm

app_name="accounts"

urlpatterns=[
path("login/",auth_views.LoginView.as_view(authentication_form=LoginForm,template_name="accounts/login.html"),name="login"),
path("logout/",auth_views.LogoutView.as_view(),name="logout"),
path("signup/",views.signup,name="signup"),
path("first_step/",views.selectinterest,name="select_interest"),
path("second_step/",views.selectprofilepicture,name="select_pic"),
path("user_profile/<str:username>/<int:pk>/",views.profileView.as_view(),name="user_profile"),
path("user_profile/change_pic/<str:username>/<int:pk>/",views.changeProfilePicView.as_view(),name="change_pic"),
path("follow/<str:username>/<int:pk>/",views.follow_view,name="follow"),
path("unfollow/<str:username>/<int:pk>/",views.unfollow_view,name="unfollow"),
path("<str:username>/<int:pk>/following",views.Following.as_view(),name="following"),
path("<str:username>/<int:pk>/Bio",views.Bio.as_view(),name="bio"),
path("interests/<str:username>/<int:pk>/",views.interestView.as_view(),name="interests"),
]
