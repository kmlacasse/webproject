from django.shortcuts import render
from django.views import View

from taapp.models import Account
from taapp.models import Course
from taapp.models import Section
from . import setup


class Home(View):
    def get(self,request):
        if "name" in request.session:
            context = {"user":request.session["name"]}
        else:
            context = {"user":None}
        return render(request, "taapp/home.html", context)

    def post(self,request):
        cmd = setup.setupCommands()
        cmd.text = request.POST["command"]
        s = cmd.callCommand(request.POST["command"])
        return render(request, "taapp/home.html", {"list":s})


class Modify(View):
    def get(self, request):
        if "name" in request.session:
            context = {"user":request.session["name"]}
        else:
            context = {"user":None}
        return render(request, "taapp/modify.html", context)

    def post(self,request):
        cmd = setup.setupCommands()
        cmd.text = request.POST["command"]
        s = cmd.callCommand(request.POST["command"])
        return render(request, "taapp/modify.html", {"list":s})


class View(View):
    def get(self, request):
        if "name" in request.session:
            context = {"user":request.session["name"]}
        else:
            context = {"user":None}
        return render(request, "taapp/view.html", context)

    def post(self,request):
        cmd = setup.setupCommands()
        cmd.text = request.POST["command"]
        s = cmd.callCommand(request.POST["command"])
        return render(request, "taapp/view.html", {"list":s})


class Login(View):
    def get(self, request):
        context = {"user": None}
        return render(request, "taapp/login.html", context)

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        cmd = setup.setupCommands()
        cmd.text = "login " + username + " " + password
        s = cmd.callCommand(cmd.text)
        # If successful login, set session name
        if s == username + " logged in":
            print("Saving session")
            request.session["name"] = username
        context = {"user":username, "list":s}
        return render(request, "taapp/login.html", context)


class Logout(View):
    def get(self, request):
        if "name" in request.session:
            context = {"user":request.session["name"]}
        else:
            context = {"user":None}
        return render(request, "taapp/logout.html", context)

    def post(self, request):
        if "name" in request.session:
            cmd = setup.setupCommands()
            cmd.text = "logout"
            s = cmd.callCommand(cmd.text)
            request.session.pop("name")
        else:
            s = "Failed. No user currently logged in"
        context = {"user": None, "list": s}
        return render(request, "taapp/logout.html", context)


class CreateCourse(View):
    def get(self, request):
        if "name" in request.session:
            context = {"user":request.session["name"]}
        else:
            context = {"user":None}
        return render(request, "taapp/create_course.html", context)

    def post(self, request):
        s = {}
        cNum = request.POST["courseNum"]
        cName = request.POST["courseName"]
        cSub = request.POST["courseSub"]
        cLecNum = request.POST["lectureNum"]
        cLabNum = request.POST["labNum"]
        cmd = setup.setupCommands()
        text = "createCourse " + cSub + cNum + " " +  cLecNum + " " + cLabNum + " " + cName
        ret = cmd.callCommand(text)
        s['response'] = ret
        return render(request, "taapp/create_course.html", {"response": s['response']})

    
class DeleteCourse(View):
    def get(self, request):
        if "name" in request.session:
            context = {"user":request.session["name"]}
            context['classes'] = list(Course.objects.values())
        else:
            context = {"user":None}
        return render(request, "taapp/delete_course.html", context)

    def post(self, request):
        s = {}
        courseid = request.POST["courseid"]
        cmd = setup.setupCommands()
        text = "deleteCourse " + courseid
        ret = cmd.callCommand(text)
        s['list'] = ret
        s['classes'] = list(Course.objects.values())

        return render(request, "taapp/delete_course.html", {"list": s['list'], "classes": s['classes']})


class CreateAccount(View):
    def get(self, request):
        # Make sure someone is logged in before showing this page
        if "name" in request.session:
            username = request.session["name"]
            context = {"user": username}
            return render(request, "taapp/create_account.html", context)
        else:
            # Redirect to login screen with error message
            s = "You must login to view this website"
            context = {"user": None, "list": s}
            return render(request, "taapp/login.html", context)

    def post(self, request):
        # Only process if someone is logged in
        if "name" in request.session:
            cmd = setup.setupCommands()
            permissions = ""
            for i in request.POST["checkbox"]:
                if i is True:
                    permissions += "1"
                else:
                    permissions += "0"
            cmd.text = "createAccount " + request.POST["username"] + " " + request.POST["password"] + permissions
            s = cmd.callCommand(request.POST["command"])
            if "Failed" in s_list:
                context = {"error": s}
            else:
                context = {"list": s}
            return render(request, "taapp/create_account.html", context)
        else:
            # If not logged in, redirect to login screen with error message
            s = "You must login to view this website"
            context = {"user": None, "list": s}
            return render(request, "taapp/login.html", context)



class EditAccount(View):
    def get(self, request):
        # Make sure someone is logged in before showing this page
        if "name" in request.session:
            username = request.session["name"]
            user = Account.objects.get(username=username)
            hasPermissions = user.permissions[0] == '1' or user.permissions[1] == '1'
            context = {"user": username, "permissions": hasPermissions, "userName": user.name, "userPassword": user.password, "userEmail": user.email, "userPhone": user.phone, "userAddress": user.address, "userHours": user.officehours}
            return render(request, "taapp/edit_account.html", context)
        else:
            # Redirect to login screen with error message
            s = "You must login to view this website"
            context = {"user": None, "list": s}
            return render(request, "taapp/login.html", context)

    def post(self, request):
        if "name" in request.session:

            cmd = setup.setupCommands()
            if request.POST["password"]:
                cmd.text = "editAccount " + request.POST["username"] + " password " + request.POST["password"]
                cmd.callCommand(request.POST["command"])
            cmd.text = "editAccount " + request.POST["username"] + " name " + request.POST["name"]
            cmd.callCommand(request.POST["command"])
            cmd.text = "editAccount " + request.POST["username"] + " address " + request.POST["address"]
            cmd.callCommand(request.POST["command"])
            cmd.text = "editAccount " + request.POST["username"] + " officehours " + request.POST["officehours"]
            cmd.callCommand(request.POST["command"])
            cmd.text = "editAccount " + request.POST["username"] + " phone " + request.POST["phone"]
            cmd.callCommand(request.POST["command"])
            cmd.text = "editAccount " + request.POST["username"] + " email " + request.POST["email"]
            s = cmd.callCommand(request.POST["command"])
            if "Failed" in s_list:
                context = {"error": s}
            else:
                context = {"list": s}
            return render(request, "taapp/edit_account.html", context)
        else:
            # If not logged in, redirect to login screen with error message
            s = "You must login to view this website"
            context = {"user": None, "list": s}
            return render(request, "taapp/login.html", context)


class DeleteAccount(View):
    def get(self, request):
        if "name" in request.session:
            context = {"user":request.session["name"]}
            context['accounts'] = list(Account.objects.values())

        else:
            context = {"user":None}
        return render(request, "taapp/delete_account.html", context)
    def post(self, request):
        s = {}
        username = request.POST["username"]
        cmd = setup.setupCommands()
        text = "deleteAccount " + username
        ret = cmd.callCommand(text)
        s['list'] = ret
        s['accounts'] = list(Account.objects.values())

        return render(request, "taapp/delete_account.html", {"list": s['list'], "accounts": s['accounts']})


class AssignInstructor(View):
    def get(self, request):
        if "name" in request.session:
            context = {"user":request.session["name"]}
        else:
            context = {"user":None, "list": ''}
        return render(request, "taapp/assign_instructor.html", context)
    def post(self, request):
        cmd = setup.setupCommands()
        cmd.text = "assignInstructor " + request.POST["username"] + " " + request.POST["courseID"] + request.POST["lecture"]
        s = cmd.callCommand(cmd.text)
        return render(request, "taapp/assign_instructor.html", {"list": s})

class AssignTA(View):
    def get(self, request):
        if "name" in request.session:
            context = {"user":request.session["name"]}
        else:
            context = {"user":None, "list": ''}
        return render(request, "taapp/assign_TA.html", context)
    def post(self, request):
        cmd = setup.setupCommands()
        cmd.text = "assignTA " + request.POST["username"] + " " + request.POST["courseID"]
        s = cmd.callCommand(cmd.text)
        return render(request, "taapp/assign_TA.html", {"list": s})


class AssignTAtoLab(View):
    def get(self, request):
        if "name" in request.session:
            context = {"user":request.session["name"]}
        else:
            context = {"user":None, "list": ''}
        return render(request, "taapp/assign_TA_to_lab.html", context)
    def post(self, request):
        cmd = setup.setupCommands()
        cmd.text = "assignTAtoLab " + request.POST["username"] + " " + request.POST["courseID"] + request.POST["lab"]
        s = cmd.callCommand(cmd.text)
        return render(request, "taapp/assign_TA_to_lab.html", {"list": s})


class ViewCourse(View):
    def get(self, request):
        if "name" in request.session:
            context = {"user":request.session["name"]}
            context['classes'] = list(Course.objects.values())

        else:
            context = {"user":None}
        return render(request, "taapp/view_course.html", context)
    def post(self, request):
        s = {}
        courseid = request.POST["courseid"]
        s['course'] = (Course.objects.get(pk=courseid))
        s['classes'] = list(Course.objects.values())

        return render(request, "taapp/view_course.html", {"course": s['course'], "classes": s['classes']})



class ViewLecture(View):
    def get(self, request):
        if "name" in request.session:
            context = {"user":request.session["name"]}

        else:
            context = {"user":None}
        return render(request, "taapp/view_lecture.html", context)
    def post(self, request):
        pass


class ViewLab(View):
    def get(self, request):
        if "name" in request.session:
            context = {"user":request.session["name"]}
        else:
            context = {"user":None}
        return render(request, "taapp/view_lab.html", context)
    def post(self, request):
        pass


class ViewAccount(View):
    def get(self, request):
        # Make sure someone is logged in before showing this page
        if "name" in request.session:
            username = request.session["name"]
            context = {"user": username}
            return render(request, "taapp/view_account.html", context)
        else:
            # Redirect to login screen with error message
            s = "You must login to view this website"
            context = {"user":None, "list":s}
            return render(request, "taapp/login.html", context)

    def post(self, request):
        # Only process if someone is logged in
        if "name" in request.session:
            username = request.session["name"]
            setup.current_user = Account.objects.get(pk=username)
            user = request.POST["name"]
            cmd = setup.setupCommands()
            cmd.text = "viewAccount " + user
            s_list = cmd.callCommand(cmd.text)
            if "Failed" in s_list:
                context = {"user": username, "error": s_list}
            elif len(s_list) > 4:
                context = {"user": username, "list_private": s_list}
            else:
                context = {"user": username, "list_public": s_list}
            return render(request, "taapp/view_account.html", context)
        else:
            # If not logged in, redirect to login screen with error message
            s = "You must login to view this website"
            context = {"user": None, "list": s}
            return render(request, "taapp/login.html", context)


class ViewUsers(View):
    def get(self, request):
        # Only process if someone is logged in
        if "name" in request.session:
            username = request.session["name"]
            setup.current_user = Account.objects.get(pk=username)
            cmd = setup.setupCommands()
            cmd.text = "viewUsers"
            s_list = cmd.callCommand(cmd.text)
            context = {"user": username, "list": s_list}
            return render(request, "taapp/view_users.html", context)
        else:
            # Redirect to login screen with error message
            s = "You must login to this website"
            context = {"user": None, "list": s}
            return render(request, "taapp/login.html", context)


class ViewInstructorAssignments(View):
    def get(self, request):
        if "name" in request.session:
            context = {"user":request.session["name"]}
        else:
            context = {"user":None, "list": ''}
        return render(request, "taapp/view_instructor_assignments.html", context)
    def post(self, request):
        cmd = setup.setupCommands()
        cmd.text = "viewInstructorAssignments " + request.POST["username"]
        s_list = cmd.callCommand(cmd.text)
        if "Failed" in s_list:
            context = {"error": s_list}
        else:
            context = {"list": s_list}
        return render(request, "taapp/view_instructor_assignments.html", context)

class ViewTAAssignments(View):
    def get(self, request):
        if "name" in request.session:
            context = {"user":request.session["name"]}
        else:
            context = {"user":None, "list": ''}
        return render(request, "taapp/view_TA_assignments.html", context)
    def post(self, request):
        cmd = setup.setupCommands()
        cmd.text = "viewTAAssignments " + request.POST["username"]
        s_list = cmd.callCommand(cmd.text)
        if "Failed" in s_list:
            context = {"error": s_list}
        else:
            context = {"list": s_list}
        return render(request, "taapp/view_TA_assignments.html", context)
