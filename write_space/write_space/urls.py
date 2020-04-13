"""write_space URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.LandingPage.as_view(),name="landing_page"),
    path("posts/",include("posts.urls",namespace="posts")),
    path("api/posts/",include("posts.api.urls",namespace="posts_api")),
    path("accounts/",include("accounts.urls",namespace="accounts")),
    path("api/token-auth/", obtain_jwt_token),
    path("api/refresh_token/",refresh_jwt_token),
    path("api/accounts/",include("accounts.api.urls",namespace="accounts_api")),
    path("accounts/",include("django.contrib.auth.urls")),
    path("about_me/",views.aboutView.as_view(),name="about_me"),


]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
