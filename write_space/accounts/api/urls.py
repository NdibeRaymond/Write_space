from django.urls import path
from . import views

app_name = "accounts_api"

urlpatterns = [
    path("signup/",views.userCreateApiView.as_view(),name="signup"),
    path("login/",views.userLoginApiView.as_view(),name="login"),
]
