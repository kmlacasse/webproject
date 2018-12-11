"""webproject URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from taapp.views.views import Home

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'home/', Home.index, name='home.html'),
    url(r'modify/', Home.index, name='modify.html'),
    url(r'view/', Home.index, name='view.html'),
    url(r'login/', Home.index, name='login.html'),
    url(r'logout/', Home.index, name='home.html'),

    path('', Home.as_view()),
]
