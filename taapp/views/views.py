from django.shortcuts import render
from django.views import View
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


class CreateCourse(View):
    def get(self, request):
        return render(request, "taapp/create_course.html")

    def post(self,request):
        cmd = setup.setupCommands()
        cmd.text = request.POST["command"]
        s = cmd.callCommand(request.POST["command"])
        return render(request, "taapp/create_course.html", {"list":s})

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
        return render(request, "taapp/assign_instructor.html", {"list":''})
    def post(self, request):
        cmd = setup.setupCommands()
        cmd.text = "assignInstructor " + request.POST["username"] + " " + request.POST["courseID"] + request.POST["lecture"]
        s = cmd.callCommand(cmd.text)
        return render(request, "taapp/assign_instructor.html", {"list": s})

class AssignTA(View):
    def get(self, request):
        return render(request, "taapp/assign_TA.html", {"list": ''})
    def post(self, request):
        cmd = setup.setupCommands()
        cmd.text = "assignTA " + request.POST["username"] + " " + request.POST["courseID"]
        s = cmd.callCommand(cmd.text)
        return render(request, "taapp/assign_TA.html", {"list": s})


class AssignTAtoLab(View):
    def get(self, request):
        return render(request, "taapp/assign_TA_to_lab.html", {"list": ''})
    def post(self, request):
        cmd = setup.setupCommands()
        cmd.text = "assignTAtoLab " + request.POST["username"] + " " + request.POST["courseID"] + request.POST["lab"]
        s = cmd.callCommand(cmd.text)
        return render(request, "taapp/assign_TA_to_lab.html", {"list": s})


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
        return render(request, "taapp/view_account.html", {"list": []})
    def post(self, request):
        user = request.POST["name"]
        cmd = setup.setupCommands()
        cmd.text = "viewAccount " + user
        s = cmd.callCommand(cmd.text)
        return render(request, "taapp/view_account.html", {"list": s})

class ViewInstructorAssignments(View):
    def get(self, request):
        return render(request, "taapp/view_instructor_assignments.html", {"list": ''})
    def post(self, request):
        cmd = setup.setupCommands()
        cmd.text = "viewAccount " + request.POST["username"]
        s = cmd.callCommand(cmd.text)
        return render(request, "taapp/view_instructor_assignments.html", {"list": s})

class ViewTAAssignments(View):
    def get(self, request):
        return render(request, "taapp/view_TA_assignments.html", {"list": ''})
    def post(self, request):
        cmd = setup.setupCommands()
        cmd.text = "viewAccount " + request.POST["username"]
        s = cmd.callCommand(cmd.text)
        return render(request, "taapp/view_TA_assignments.html", {"list": s})