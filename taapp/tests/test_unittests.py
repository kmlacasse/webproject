from django.test import TestCase
from taapp.models import Account
from taapp.models import Course
from taapp.models import Section
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
        course = Course.objects.create(courseID="01361", courseName="Introduction to Software Engineering", lectureSectionCount=1, labSectionCount=1)
        Section.objects.create(sectionID="013611", sectionName="Introduction to Software Engineering - Lecture 1", sectionType=1, parentCourse=course)
        Section.objects.create(sectionID="01361101", sectionName="Introduction to Software Engineering - Lab 1", sectionType=0, parentCourse=course)


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

class TestAssignInstructor(BaseCase):

    # Unit Tests for assignInstructor command

    def testAssignInstructorSuccessAndDup(self):
        #login super
        self.cmd.callCommand("login john super")

        #assign bill to lecture 013611
        ret = self.cmd.callCommand("assignInstructor bill 013611")
        self.assertEqual(ret, "bill successfully assigned to lecture.")

        #attempt to assign bill again
        ret = self.cmd.callCommand("assignInstructor bill 013611")
        self.assertEqual(ret, "Failed. Lecture already assigned an instructor.")

    def testAssignInstructorInvalid(self):
        #no user logged in
        ret = self.cmd.callCommand("assignInstructor bill 013611")
        self.assertEqual(ret, "Failed. No user currently logged in.")

        #login super
        self.cmd.callCommand("login john super")

        #invalid parameters
        ret = self.cmd.callCommand("assignInstructor bill")
        self.assertEqual(ret, "Failed. Invalid parameters.")

        #No such user
        ret = self.cmd.callCommand("assignInstructor xyz 013611")
        self.assertEqual(ret, "Failed. No such username.")

        #username is not an instructor
        ret = self.cmd.callCommand("assignInstructor rick 013611")
        self.assertEqual(ret, "Failed. Username is not an instructor.")

        #course does not exist
        ret = self.cmd.callCommand("assignInstructor bill 000001")
        self.assertEqual(ret, "Failed. Course does not exist.")

        #logout super
        self.cmd.callCommand("logout")

        #login non super
        self.cmd.callCommand("login bill instructor")

        #attempt to assigninstructor
        ret = self.cmd.callCommand("assignInstructor bill 013611")
        self.assertEqual(ret, "Failed. Restricted action.")

class TestAssignTA(BaseCase):

    # Unit Tests for assignTA command

    def testAssignTASuccess(self):
        #login super
        self.cmd.callCommand("login john super")

        #assign ian to course 01361
        ret = self.cmd.callCommand("assignTA ian 01361")
        self.assertEqual(ret, "ian successfully assigned to course.")

    def testAssignTAInvalid(self):
        #no user logged in
        ret = self.cmd.callCommand("assignTA ian 01361")
        self.assertEqual(ret, "Failed. No user currently logged in.")

        #login super
        self.cmd.callCommand("login john super")

        #invalid parameters
        ret = self.cmd.callCommand("assignTA ian 01361 extra")
        self.assertEqual(ret, "Failed. Invalid parameters.")

        #No such user
        ret = self.cmd.callCommand("assignTA xyz 01361")
        self.assertEqual(ret, "Failed. No such username.")

        #username is not an TA
        ret = self.cmd.callCommand("assignTA rick 01361")
        self.assertEqual(ret, "Failed. Username is not an TA.")

        #course does not exist
        ret = self.cmd.callCommand("assignTA ian 00001")
        self.assertEqual(ret, "Failed. Course does not exist.")

        #logout super
        self.cmd.callCommand("logout")

        #login non super
        self.cmd.callCommand("login ian TA")

        #attempt to assignTA
        ret = self.cmd.callCommand("assignTA ian 01361")
        self.assertEqual(ret, "Failed. Restricted action.")

class TestAssignTAtoLab(BaseCase):

    # Unit Tests for assignTAtoLab command

    def testAssignTAtoLabSuccessAndDup(self):
        #login super
        self.cmd.callCommand("login john super")

        #assign ian to lab 01361101
        ret = self.cmd.callCommand("assignTAtoLab ian 01361101")
        self.assertEqual(ret, "ian successfully assigned to lab.")

        #attempt to assign ian again
        ret = self.cmd.callCommand("assignTAtoLab ian 01361101")
        self.assertEqual(ret, "Failed. Lab already assigned a TA.")

    def testAssignTAtoLabInvalid(self):
        #no user logged in
        ret = self.cmd.callCommand("assignTAtoLab ian 01361101")
        self.assertEqual(ret, "Failed. No user currently logged in.")

        #login super
        self.cmd.callCommand("login john super")

        #invalid parameters
        ret = self.cmd.callCommand("assignTA")
        self.assertEqual(ret, "Failed. Invalid parameters.")

        #No such user
        ret = self.cmd.callCommand("assignTAtoLab xyz 01361101")
        self.assertEqual(ret, "Failed. No such username.")

        #username is not an TA
        ret = self.cmd.callCommand("assignTAtoLab rick 01361101")
        self.assertEqual(ret, "Failed. Username is not an TA.")

        #course does not exist
        ret = self.cmd.callCommand("assignTAtoLab ian 00000000")
        self.assertEqual(ret, "Failed. Course does not exist.")

        #logout super
        self.cmd.callCommand("logout")

        #login non super
        self.cmd.callCommand("login ian TA")

        #attempt to assignTAtoLab
        ret = self.cmd.callCommand("assignTAtoLab ian 01361101")
        self.assertEqual(ret, "Failed. Restricted action.")