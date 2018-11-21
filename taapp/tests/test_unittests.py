from django.test import TestCase
from taapp.models import Account
from taapp.views import setup

""""
These are the Unit Tests for the TA Scheduling App for Team 404
"""


class BaseCase(TestCase):
    # Use this to setup tests for all cases
    def setUp(self):
        self.cmd = setup.setupCommands()
        Account.objects.create(username="john", name="John", password="super", permissions="1000", email="john@uwm.edu", phone="41412344567", address="123 Cramer St., Milwaukee, WI  53211")
        Account.objects.create(username="rick", name="Rick", password="admin", permissions="0100", email="rick@uwm.edu", phone="2627654321", address="456 Kenwood Blvd., Milwaukee, WI  53211")
        Account.objects.create(username="bill", name="Bill", password="instructor", permissions="0010", email="bill@uwm.edu", phone="4140241357", address="789 Downer Ave., Milwaukee, WI  53211", officehours="Tuesday 5-6pm")
        Account.objects.create(username="ian", name="Ian", password="TA", permissions="0001", email="ian@uwm.edu", phone="4149756420", address="901 Newport Ave., Milwaukee, WI  53211", officehours="MW 11am - Noon")


class TestLogin(BaseCase):

    # Unit Tests for the login command

    def testLoginInvalid(self):
        # John attempts to login with the wrong password
        ret = self.cmd.callCommand ("login john notme")
        self.assertEqual(ret, "Failed. Username or password invalid")

        # John attempts to login with an incorrect username
        ret = self.cmd.callCommand ("login 34 super")
        self.assertEqual(ret, "Failed. No such username")

        # John attempts to login without all parameters
        ret = self.cmd.callCommand ("login john")
        self.assertEqual(ret, "Failed. Invalid parameters")

        # John attempts to login with too many parameters
        ret = self.cmd.callCommand ("login john super extra")
        self.assertEqual(ret, "Failed. Invalid parameters")

    def testLoginSuccessAndDuplicate(self):
        # John logs in with a supervisor account
        ret = self.cmd.callCommand ("login john super")
        self.assertEqual(ret, "john logged in")

        # John attempts to login again
        ret = self.cmd.callCommand ("login john super")
        self.assertEqual(ret, "Failed. User currently logged in")


class TestLogout(BaseCase):

    # Unit Tests for the logout command

    def testLogout(self):
        # John is logged in
        setup.current_user = Account.objects.get(username="john")

        # John attempts to logout but passes too many parameters
        ret = self.cmd.callCommand("logout extra")
        self.assertEqual(ret, "Failed. Invalid parameters")

        # John logs out
        ret = self.cmd.callCommand("logout")
        self.assertEqual(ret, "Goodbye")

        # Attempt to logout with no user logged in
        ret = self.cmd.callCommand("logout")
        self.assertEqual(ret, "Failed. No current user to log out")
