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
from taapp.views.views import *

urlpatterns = [
    url(r'admin/', admin.site.urls),
    path(r'home.html', Home.as_view()),
    path(r'modify.html', Modify.as_view()),
    path(r'view.html', View.as_view()),
    path(r'login.html', Login.as_view()),
    path(r'logout.html', Logout.as_view()),
    path(r'create_course.html', CreateCourse.as_view()),
    path(r'delete_course.html', DeleteCourse.as_view()),
    path(r'create_account.html', CreateAccount.as_view()),
    path(r'edit_account.html', EditAccount.as_view()),
    path(r'delete_account.html', DeleteAccount.as_view()),
    path(r'assign_instructor.html', AssignInstructor.as_view()),
    path(r'assign_TA.html', AssignTA.as_view()),
    path(r'assign_TA_to_lab.html', AssignTAtoLab.as_view()),
    path(r'view_course.html', ViewCourse.as_view()),
    path(r'view_lecture.html', ViewLecture.as_view()),
    path(r'view_lab.html', ViewLab.as_view()),
    path(r'view_account.html', ViewAccount.as_view()),
    path(r'view_instructor_assignments.html', ViewInstructorAssignments.as_view()),
    path(r'view_TA_assignments.html', ViewTAAssignments.as_view()),
    path('', Home.as_view()),

]
