"""ebdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("account/", views.account_request, name="account"),
    path("challenges/issue/", views.challenges_issue, name="challenge_issue"),
    path("challenges/accept/<challenge_slug>/", views.challenges_accept, name="challenge_respond"),
    path("challenges/decline/<challenge_slug>/", views.challenges_decline, name="challenge_respond"),
    path("challenges/", views.challenges_request, name="challenges"),
    path("active/", views.active_request, name="active"),
    path("active/<active_slug>/resign", views.active_slug_resign, name="active_resign"),
    path("active/<active_slug>/", views.active_slug, name="active_slug"),
    path("ai/", views.ai_request, name="ai"),
    path("study/", views.study_request, name="study"),
    path("local/", views.local_request, name="local"),
    path("game/<single_slug>/", views.single_slug, name="single_slug"),
]
