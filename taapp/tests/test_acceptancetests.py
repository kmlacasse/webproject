from django.test import TestCase
from taapp.models import Account
from taapp.views import setup

""""
These are the Acceptance Tests for the TA Scheduling App for Team 404
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
    # AT for PBI:  As a user, I want to login so I can issue commands

    def testLogin(self):
        # John has a supervisor account
        # John logs in
        ret = self.cmd.callCommand("login john super")
        self.assertEqual(ret, "john logged in")
        # Try logging in again to verify that it is not possible because you are already logged in
        ret = self.cmd.callCommand("login john super")
        self.assertEqual(ret, "Failed. User currently logged in")
