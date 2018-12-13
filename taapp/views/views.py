from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from taapp.forms import *
from . import setup


class Home(View):
    def get(self,request):
        return render(request, "taapp/home.html")

    def post(self,request):
        cmd = setup.setupCommands()
        cmd.text = request.POST["command"]
        s = cmd.callCommand(request.POST["command"])
        return render(request, "taapp/home.html", {"list":s})


class Modify(View):
    def get(self, request):
        return render(request, "taapp/modify.html")

    def post(self,request):
        cmd = setup.setupCommands()
        cmd.text = request.POST["command"]
        s = cmd.callCommand(request.POST["command"])
        return render(request, "taapp/modify.html", {"list":s})


class View(View):
    def get(self, request):
        return render(request, "taapp/view.html")

    def post(self,request):
        cmd = setup.setupCommands()
        cmd.text = request.POST["command"]
        s = cmd.callCommand(request.POST["command"])
        return render(request, "taapp/view.html", {"list":s})


class Login(View):
    def get(self, request):
        return render(request, "taapp/login.html")

    def post(self, request):
        pass


class Logout(View):
    def get(self, request):
        return render(request, "taapp/logout.html")

    def post(self, request):
        pass


class CreateCourse(View):
    def get(self, request):
        form = createCourseForm()
        return render(request, "taapp/create_course.html", {'form':form})

    def post(self, request):
        form = createCourseForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']
            #Trying to find a way to print this data so I can see it so I know before if I am actually going to pass anything
            form = createCourseForm()


        args = {'response':list} #This is where I would pass the response if it was successful or not
        return render(request, "taapp/create_course.html", args)

class DeleteCourse(View):
    def get(self, request):
        return render(request, "taapp/delete_course.html")

    def post(self, request):
        cmd = setup.setupCommands()
        cmd.text = request.POST["command"]
        s = cmd.callCommand(request.POST["command"])
        return render(request, "taapp/delete_course.html", {"list":s})

class CreateAccount(View):
    def get(self, request):
        return render(request, "taapp/create_account.html")
    def post(self, request):
        pass


class EditAccount(View):
    def get(self, request):
        return render(request, "taapp/edit_account.html")
    def post(self, request):
        pass


class DeleteAccount(View):
    def get(self, request):
        return render(request, "taapp/delete_account.html")
    def post(self, request):
        pass


class AssignInstructor(View):
    def get(self, request):
        return render(request, "taapp/assign_instructor.html")
    def post(self, request):
        pass

class AssignTA(View):
    def get(self, request):
        return render(request, "taapp/assign_TA.html")
    def post(self, request):
        pass


class AssignTAtoLab(View):
    def get(self, request):
        return render(request, "taapp/assign_TA_to_lab.html")
    def post(self, request):
        pass


class ViewCourse(View):
    def get(self, request):
        return render(request, "taapp/view_course.html")
    def post(self, request):
        pass


class ViewLecture(View):
    def get(self, request):
        return render(request, "taapp/view_lecture.html")
    def post(self, request):
        pass


class ViewLab(View):
    def get(self, request):
        return render(request, "taapp/view_lab.html")
    def post(self, request):
        pass


class ViewAccount(View):
    def get(self, request):
        return render(request, "taapp/view_account.html")
    def post(self, request):
        pass