"""
URL configuration for sharingapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path

from sharing import views


urlpatterns = [
    path('', views.index, name='index'),
    #path('sharing/', include('sharing.urls')),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('sign_up/', views.signup_view, name='signup_view'),
    path('chat/', views.chat_view, name='chat_view'),
    # path('main/', views.main),
    # path('jump/', views.jump),
    # path('plan/', views.plan),
    # path('hardware/', views.Hardware_View.as_view()),
    # path('send_email/', views.send_email)
]