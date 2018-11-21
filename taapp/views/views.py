from django.shortcuts import render
from django.views import View
from . import setup


class Home(View):
    def get(self,request):
        return render(request, "taapp/index.html")

    def post(self,request):
        cmd = setup.setupCommands()
        cmd.text = request.POST["command"]
        s = cmd.callCommand(request.POST["command"])
        return render(request, "taapp/index.html", {"list":s})

    def index(self, request):
        return render(request, "taapp/index.html")
