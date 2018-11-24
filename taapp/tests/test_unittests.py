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
        setup.current_user = None
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


class TestViewAccount(BaseCase):

    # Unit Tests for the viewAccount command

    def testViewAccountInvalid(self):
        # John attempts to view account without being logged in
        ret = self.cmd.callCommand("viewAccount bill")
        self.assertEqual(ret, "Failed. No user currently logged in")

        # John is logged in
        setup.current_user = Account.objects.get(username="john")

        # John attempts to view a username that does not exist
        ret = self.cmd.callCommand("viewAccount person")
        self.assertEqual(ret, "Failed. No account person")

        # John attempts to view account without all parameters
        ret = self.cmd.callCommand("viewAccount")
        self.assertEqual(ret, "Failed. Invalid parameters")

        # John attempts to view account with too many parameters
        ret = self.cmd.callCommand("viewAccount bill extra")
        self.assertEqual(ret, "Failed. Invalid parameters")

    def testViewAccountValid(self):
        # John is logged in
        setup.current_user = Account.objects.get(username="john")

        # John views an account and can see the private information
        ret = self.cmd.callCommand("viewAccount bill")
        self.assertIn("Downer", ret)

        # Now Rick is logged in instead
        setup.current_user = Account.objects.get(username="rick")

        # Bill views an account and can see the private information
        ret = self.cmd.callCommand("viewAccount john")
        self.assertIn("Cramer", ret)

        # Now Bill is logged in instead
        setup.current_user = Account.objects.get(username="bill")

        # Bill views an account and can only see the public information
        ret = self.cmd.callCommand("viewAccount john")
        self.assertIn("John", ret)
        self.assertNotIn("Cramer", ret)

        # Now Ian is logged in instead
        setup.current_user = Account.objects.get(username="ian")

        # Ian views an account and can only see the public information
        ret = self.cmd.callCommand("viewAccount john")
        self.assertIn("John", ret)
        self.assertNotIn("Cramer", ret)


class TestCreateAccount(BaseCase):

    # Unit Tests for the create account command

    def testSupervisorCreateAccount(self):
        # John logs in with a supervisor account
        setup.current_user = Account.objects.get(username="john")

        # John creates an account which does not yet exist
        ret = self.cmd.callCommand("createAccount tim default 1000")
        self.assertEqual(ret, "Account tim successfully added")

        # John attempts to create a duplicate account
        ret = self.cmd.callCommand("createAccount tim default 1000")
        self.assertEqual(ret, "Failed. Username currently in use")

        # John logs out
        setup.current_user = None

    def testCreateAccountInvalidArguments(self):
        # John logs in with a supervisor account
        setup.current_user = Account.objects.get(username="john")

        # John passes 0 of 3 arguments
        ret = self.cmd.callCommand("createAccount")
        self.assertEqual(ret, "Failed. Invalid parameters")

        # John only passes 1 of 3 arguments
        ret = self.cmd.callCommand("createAccount todd")
        self.assertEqual(ret, "Failed. Invalid parameters")

        # John only passes 2 of 3 arguments
        ret = self.cmd.callCommand("createAccount todd default")
        self.assertEqual(ret, "Failed. Invalid parameters")

        # John passes too many arguments
        ret = self.cmd.callCommand("createAccount todd default 1000 extra")
        self.assertEqual(ret, "Failed. Invalid parameters")

        # John passes an invalid account type for the last argument
        ret = self.cmd.callCommand("createAccount todd default 0002")
        self.assertEqual(ret, "Failed. Invalid parameters")

        # John passes a character for the last parameter, which should be a number
        ret = self.cmd.callCommand("createAccount todd default 000b")
        self.assertEqual(ret, "Failed. Invalid parameters")

        # John logs out
        setup.current_user = None

    def testAdministratorCreateAccount(self):
        # Rick logs into an administrator account
        setup.current_user = Account.objects.get(username="rick")

        # Rick creates an account which does not yet exist
        ret = self.cmd.callCommand("createAccount jim default 1000")
        self.assertEqual(ret, "Account jim successfully added")

        # Rick logs out
        setup.current_user = None

    def testNoUserCreateAccount(self):
        # With no one logged in, attempt to create an account
        ret = self.cmd.callCommand("createAccount sam default 1000")
        self.assertEqual(ret, "Failed. No user currently logged in")

    def testInstructorCreateAccount(self):
        # Bill logs into an instructor account
        setup.current_user = Account.objects.get(username="bill")

        # Bill attempts to create an account
        ret = self.cmd.callCommand("createAccount sam default 1000")
        self.assertEqual(ret, "Failed. Restricted action")

        # Bill logs out
        setup.current_user = None

    def testTACreateAccount(self):
        # Ian logs into a TA account
        setup.current_user = Account.objects.get(username="ian")

        # Ian attempts to create an account
        ret = self.cmd.callCommand("createAccount sam default 1000")
        self.assertEqual(ret, "Failed. Restricted action")

        # Ian logs out
        setup.current_user = None
