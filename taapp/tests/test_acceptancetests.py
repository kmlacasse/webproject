from django.test import TestCase
from unittest import skip
from taapp.models import Account, Course, Section, CourseMember, SectionMember
from taapp.views import setup

""""
These are the Acceptance Tests for the TA Scheduling App for Team 404
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
    # AT for PBI:  As a user, I want to login so I can issue commands

    def testLogin(self):
        # John has a supervisor account
        # John logs in
        ret = self.cmd.callCommand("login john super")
        self.assertEqual(ret, "john logged in")
        # Try logging in again to verify that it is not possible because you are already logged in
        ret = self.cmd.callCommand("login john super")
        self.assertEqual(ret, "Failed. User currently logged in")


class TestLogout(BaseCase):
    # AT for PBI:  As a user, I want to logout so others don't issue commands as me

    def testLogout(self):
        # John has a supervisor account
        # John logs in
        self.cmd.callCommand("login john super")
        # John logs out
        ret = self.cmd.callCommand("logout")
        self.assertEqual(ret, "Goodbye")
        # Try to issue a command to verify that John is logged out
        ret = self.cmd.callCommand("logout")
        self.assertEqual(ret, "Failed. No current user to log out")


@skip("Wait for the viewCourse command")
class TestSupervisorCreateCourse(BaseCase):
    # AT for PBI:  As a Supervisor, I want to create a course

    def tearDown(self):
        # Remove the created course
        self.cmd.callCommand("deleteCourse 01361")

    def testSupervisorCreateCourse(self):
        # John has a supervisor account
        # John logs in
        self.cmd.callCommand("login john super")
        # John creates a course which does not yet exist
        ret = self.cmd.callCommand("createCourse 01361 1 3 Introduction to Software Engineering")
        self.assertEqual(ret, "Course Introduction to Software Engineering  successfully added")
        # Verify course was created by viewing it
        ret = self.cmd.callCommand("viewCourse 01361")
        self.assertIn("Introduction to Software Engineering", ret)


class TestSupervisorDeleteCourse(BaseCase):
    # AT for PBI:  As a Supervisor, I want to delete a course

    def testSupervisorDeleteCourse(self):
        # John has a supervisor account
        # John logs in
        self.cmd.callCommand("login john super")
        # John creates a course which will be deleted
        ret = self.cmd.callCommand("createCourse 01361 1 3 Introduction to Software Engineering")
        # John deletes the course
        ret = self.cmd.callCommand("deleteCourse 01361")
        self.assertEqual(ret, "Course 01361 successfully removed.")
        # Attempt to view course to verify that it is not there
        ret = self.cmd.callCommand("viewCourse 01361")
        self.assertEqual(ret, "Failed. Course does not exists")


class TestSupervisorCreateAccount(BaseCase):
    # AT for PBI:  As a Supervisor, I want to create an account

    def tearDown(self):
        # Remove the created account
        self.cmd.callCommand("deleteAccount tim")

    def testSupervisorCreateAccount(self):
        # John has a supervisor account
        # John logs in
        self.cmd.callCommand("login john super")
        # John creates an account which does not yet exist
        ret = self.cmd.callCommand("createAccount tim default 1000")
        self.assertEqual(ret, "Account tim successfully added")
        # Login to new account to verify that it was created
        self.cmd.callCommand("logout")
        ret = self.cmd.callCommand("login tim default")
        self.assertEqual(ret, "tim logged in")


class TestSupervisorDeleteAccount(BaseCase):
    # AT for PBI:  As a Supervisor, I want to delete an account


    def testSupervisorDeleteAccount(self):
        # John has a supervisor account
        # John logs in
        self.cmd.callCommand("login john super")
        # Create the user account that will be deleted
        self.cmd.callCommand("createAccount tim default 0010")
        # John deletes an account for an existing user
        ret = self.cmd.callCommand("deleteAccount tim")
        self.assertEqual(ret, "Account tim successfully removed.")
        # Try to login to account to verify that it does not exist
        self.cmd.callCommand("logout")
        ret = self.cmd.callCommand("login tim default")
        self.assertEqual(ret, "Failed. No such username")


@skip("Save for a future Sprint")
class TestSupervisorEditAccount(BaseCase):
    # AT for PBI:  As a Supervisor, I want to edit an account

    def tearDown(self):
        # Remove the created and modified account
        self.cmd.callCommand("deleteAccount tim")

    def testSupervisorEditAccount(self):
        # John has a supervisor account
        # John logs in
        self.cmd.callCommand("login john super")
        # Create the user account that will be modified
        self.cmd.callCommand("createAccount tim default 0100")
        # John edits an account for an existing user
        ret = self.cmd.callCommand("editAccount tim")
        # Assume John made a change to the account
        self.assertEqual(ret, "Account tim successfully modified")
        # View account to verify that changes are shown
        ret = self.cmd.callCommand("viewAccount tim")
        self.assertEqual(ret, "tim: all information")
        # Assume John can see the account changes


@skip("Save for a future Sprint")
class TestSupervisorEmailUsers(BaseCase):
    # AT for PBI:  As a supervisor, I want to send out notifications to users via UWM email

    def testSupervisorEmailUsers(self):
        # John has a supervisor account
        # John logs in
        self.cmd.callCommand("login john super")
        # Assume there are a set of users with email addresses
        # John sends an email notification
        ret = self.cmd.callCommand("sendNotification users 'This is a test message'")
        self.assertEqual(ret, "Email successfully sent to users")


@skip("Save for a future Sprint")
class TestSupervisorViewCourse(BaseCase):
    # AT for PBI:  As a supervisor, I want to see the number of sections per course,
    # to determine the minimum number of instructors to assign

    # Also AT for PBI:  As a supervisor, I would like to be able to see the number of lab sections,
    # so that I know the minimum number of TAs required

    def tearDown(self):
        # Remove the created course
        self.cmd.callCommand("deleteCourse 01361")

    def testSupervisorViewCourse(self):
        # John has a supervisor account
        # John logs in
        self.cmd.callCommand("login john super")
        # Create a course which will be viewed
        self.cmd.callCommand("createCourse 01361 1 3 Introduction to Software Engineering")
        # John views a course which exists
        ret = self.cmd.callCommand("viewCourse 01361")
        self.assertIn("Introduction to Software Engineering", ret)


@skip("Save for a future Sprint")
class TestSupervisorViewInstructorAssignments(BaseCase):
    # AT for PBI:  As a supervisor, I want to be able to see the previous courses an instructor has taught,
    # so that I may determine which courses should be assigned to them

    # Also AT for PBI:  As a supervisor, I want to be able to see the teaching schedule of an instructor,
    # so that I may avoid assigning them to multiple sections

    def tearDown(self):
        # Delete the course and instructor created
        self.cmd.callCommand("deleteCourse 01361")
        self.cmd.callCommand("deleteAccount tim")

    def testSupervisorViewInstructorAssignments(self):
        # John has a supervisor account
        # John logs in
        self.cmd.callCommand("login john super")
        # Create a course
        self.cmd.callCommand("createCourse 01361 'Introduction to Software Engineering' 1 3")
        # Create an instructor
        self.cmd.callCommand("createAccount tim default 0010")
        # Assign a course to an instructor
        self.cmd.callCommand("assignInstructor tim 01361")
        # John views the courses assigned to an instructor which exists
        ret = self.cmd.callCommand("viewAssignmentInstructor tim")
        self.assertIn("Introduction to Software Engineering", ret)


@skip("Wait for this to be implemented")
class TestSupervisorAssignTAtoCourse(BaseCase):
    # AT for PBI:  As a supervisor, I would like to be able to assign TAs to courses,
    # so that each course would have sufficient number of TAs

    def tearDown(self):
        # Delete the course and TA created
        self.cmd.callCommand("deleteCourse 01361")
        self.cmd.callCommand("deleteAccount ian")

    def testSupervisorAssignTAtoCourse(self):
        # John has a supervisor account
        # John logs in
        self.cmd.callCommand("login john super")
        # Create a course
        self.cmd.callCommand("createCourse 01361 1 3 Introduction to Software Engineering")
        # Create a TA
        self.cmd.callCommand("createAccount ian pass123 0001")
        # John assigns a TA to a course
        ret = self.cmd.callCommand("assignTA ian 01361")
        self.assertIn("ian successfully assigned", ret)
        # View course to verify that TA is listed
        ret = self.cmd.callCommand("viewCourse 01361")
        self.assertIn("ian", ret)


@skip("Wait for assign TA to Lab command")
class TestSupervisorAssignTAtoLab(BaseCase):
    # AT for PBI:  As a supervisor, I would like to be able to assign TAs to specific lab sections,
    # so that TAs can work around their schedule

    def tearDown(self):
        # Delete the course and TA created
        self.cmd.callCommand("deleteCourse 01361")
        self.cmd.callCommand("deleteAccount ian")

    def testSupervisorAssignTAtoLab(self):
        # John has a supervisor account
        # John logs in
        self.cmd.callCommand("login john super")
        # Create a course
        self.cmd.callCommand("createCourse 01361 1 3 Introduction to Software Engineering")
        # Create a TA
        self.cmd.callCommand("createAccount ian pass123 0001")
        # John assigns a TA to a lab section
        ret = self.cmd.callCommand("assignTAtoLab ian 01361 1")
        self.assertIn("ian successfully assigned", ret)
        # View course to verify that TA is listed
        ret = self.cmd.callCommand("viewCourse 01361")
        self.assertIn("ian", ret)


@skip("Wait for this to be implemented")
class TestSupervisorAssignInstructortoCourse(BaseCase):
    # AT for PBI:  As a supervisor, I want to assign an instructor to a course

    def tearDown(self):
        # Delete the course and instructor created
        self.cmd.callCommand("deleteCourse 01361")
        self.cmd.callCommand("deleteAccount tim")

    def testSupervisorAssignTAtoLab(self):
        # John has a supervisor account
        # John logs in
        self.cmd.callCommand("login john super")
        # Create a course
        self.cmd.callCommand("createCourse 01361 1 3 Introduction to Software Engineering")
        # Create an instructor
        self.cmd.callCommand("createAccount tim default 0010")
        # John assigns an instructor to a course
        ret = self.cmd.callCommand("assignInstructor tim 01361")
        self.assertIn("tim successfully assigned", ret)
        # View course to verify that instructor is listed
        ret = self.cmd.callCommand("viewCourse 01361")
        self.assertIn("tim", ret)


@skip("Wait for viewCourse")
class TestAdministratorCreateCourse(BaseCase):
    # AT for PBI:  As an administrator, I want to create a course

    def tearDown(self):
        # Remove the created course
        self.cmd.callCommand("deleteCourse 01361")

    def testAdministratorCreateCourse(self):
        # Rick has an administrator account
        # Rick logs in
        self.cmd.callCommand("login rick admin")
        # Rick creates a course which does not yet exist
        ret = self.cmd.callCommand("createCourse 01361 1 3 Introduction to Software Engineering")
        self.assertEqual(ret, "Course Introduction to Software Engineering  successfully added")
        # Verify course was created by viewing it
        ret = self.cmd.callCommand("viewCourse 01361")
        self.assertIn("Introduction to Software Engineering", ret)


class TestAdministratorDeleteCourse(BaseCase):
    # AT for PBI:  As an administrator, I want to delete a course

    def testAdministratorDeleteCourse(self):
        # Rick has an administrator account
        # John logs in
        self.cmd.callCommand("login rick admin")
        # Rick creates a course which will be deleted
        ret = self.cmd.callCommand("createCourse 01361 1 3 Introduction to Software Engineering")
        # Rick deletes the course
        ret = self.cmd.callCommand("deleteCourse 01361")
        self.assertEqual(ret, "Course 01361 successfully removed.")
        # Attempt to view course to verify that it is not there
        ret = self.cmd.callCommand("viewCourse 01361")
        self.assertEqual(ret, "Failed. Course does not exists")


class TestAdministratorCreateAccount(BaseCase):
    # AT for PBI:  As an administrator, I want to create an account

    def tearDown(self):
        # Remove the created account
        self.cmd.callCommand("deleteAccount tim")

    def testAdministratorCreateAccount(self):
        # Rick has an administrator account
        # Rick logs in
        self.cmd.callCommand("login rick admin")
        # Rick creates an account which does not yet exist
        ret = self.cmd.callCommand("createAccount tim default 1000")
        self.assertEqual(ret, "Account tim successfully added")
        # Login to new account to verify that it was created
        self.cmd.callCommand("logout")
        ret = self.cmd.callCommand("login tim default")
        self.assertEqual(ret, "tim logged in")


class TestAdministratorDeleteAccount(BaseCase):
    # AT for PBI:  As an administrator, I want to delete an account

    def testAdministratorDeleteAccount(self):
        # Rick has an administrator account
        # Rick logs in
        self.cmd.callCommand("login rick admin")
        # Create the user account that will be deleted
        self.cmd.callCommand("createAccount tim default 0010")
        # Rick deletes an account for an existing user
        ret = self.cmd.callCommand("deleteAccount tim")
        self.assertEqual(ret, "Account tim successfully removed.")
        # Try to login to account to verify that it does not exist
        self.cmd.callCommand("logout")
        ret = self.cmd.callCommand("login tim default")
        self.assertEqual(ret, "Failed. No such username")


@skip("Save for a future Sprint")
class TestAdministratorEditAccount(BaseCase):
    # AT for PBI:  As an administrator, I want to edit an account

    def tearDown(self):
        # Remove the created and modified account
        self.cmd.callCommand("deleteAccount tim")

    def testAdministratorEditAccount(self):
        # Rick has an administrator account
        # Rick logs in
        self.cmd.callCommand("login rick admin")
        # Create the user account that will be modified
        self.cmd.callCommand("createAccount tim default 0010")
        # Rick edits an account for an existing user
        ret = self.cmd.callCommand("editAccount tim")
        # Assume Rick changes the account
        self.assertEqual(ret, "Account tim successfully modified")
        # View account to verify that changes are shown
        ret = self.cmd.callCommand("viewAccount tim")
        self.assertEqual(ret, "tim: all information")
        # Assume Rick can see the account changes


@skip("Save for a future Sprint")
class TestAdministratorEmailUsers(BaseCase):
    # AT for PBI:  As an administrator, I want to send out notifications to users via UWM email

    def testAdministratorEmailUsers(self):
        # Rick has an administrator account
        # Rick logs in
        self.cmd.callCommand("login rick admin")
        # Assume there are a set of users with email addresses
        # Rick sends an email notification
        ret = self.cmd.callCommand("sendNotification users 'This is a test message'")
        self.assertEqual(ret, "Email successfully sent to users")


@skip("Save for a future Sprint")
class TestInstructorViewTA(BaseCase):
    # AT for PBI: As an instructor, I want to view the TA's assigned to my courses

    def testInstructorViewTA(self):
        # Asssume Bill is an Instructor
        # Bill logs in
        self.cmd.callCommand("login bill instructor")

        # Assume there is a course with ID 01361
        # Assume Bill is an instructor of said course
        # Assume bob is a TA of said course
        ret = self.cmd.callCommand("viewCourse 01361")
        self.assertIn("bob", ret)
        ret = self.cmd.callCommand("assignTAtoLab tim")
        self.assertEqual(ret, "bob successfully assigned to lab section")


@skip("Save for a future Sprint")
class TestInstructorEditPersonalInfo(BaseCase):
    # At for PBI: As an Instructor, I want to edit my personal contact information

    def testInstructorEditPersonalInfo(self):
        #Assume Bill is an Instructor
        #Bill logs in
        self.cmd.callCommand("login bill instructor")

        ret = self.cmd.callCommand("editAccount bill")
        self.assertEqual("Account bill successfully modified", ret)
        ret = self.cmd.callCommand("viewAccount bill")
        #Assuming bill changed his phone number to (414)555-5555
        self.assertIn("(414)555-5555", ret)


@skip("Save for a future Sprint")
class TestInstructorViewAssignmentInstructor(BaseCase):
    # AT for PBI: As an instuctor, I want to view the courses I am assigned to

    def testInstructorViewAssignmentInstructor(self):
        #assume Bill is an Instructor
        #Bill logs in
        self.cmd.callCommand("login bill instructor")

        #Assume bill is already assigned to class 01361
        ret = self.cmd.callCommand("viewAssignmentInstructor bill")
        self.assertIn("Introduction to Software Engineering", ret)


@skip("Save for a future Sprint")
class TestInstructorSendEmail(BaseCase):
    # AT for PBI: As an instructor, I want to be able to send out notifications to my TAs via UWM email

    def testInstructorSendEmail(self):
        #assume Bill is an Instructor
        self.cmd.callCommand("login bill instructor")

        #assume Bill is already assigned to course 01361
        ret = self.cmd.callCommand("sendNotificationTA 01361 'This is a test message'")
        self.assertEqual(ret, "Email successfully sent to TAs of Intro to Software Engineering.")


@skip("Wait for this to be implemented")
class TestInstructorAssignTAtoLab(BaseCase):
    # AT for PBI: As an Instructor, I want to be able to assign my TAS to particular lab sections

    def testInstructorAssignTAtoLab(self):
        #assume Bill is an Instructor
        self.cmd.callCommand("login bill instructor")

        #assume Bill is already assigned to course 01361
        #assume TA Bob is assigned to course 01361
        ret = self.cmd.callCommand("assignTA bob 01361 01")
        self.assertEqual(ret, "bob successfully assigned")
        ret = self.cmd.callCommand("viewCourse 01361")
        self.assertIn("01 - bob", ret)



class TestInstructorViewPublicInfo(BaseCase):
    # AT for PBI: As an instructor, I want to be able to read public contact information of all users

    def testInstructorViewPublicInfo(self):
        #Asssume Bill is an Instructor
        self.cmd.callCommand("login bill instructor")

        #Assume TA ian and Supervisor john exists
        ret = self.cmd.callCommand("viewAccount ian")
        self.assertIn("ian", ret)
        ret = self.cmd.callCommand("viewAccount john")
        self.assertIn("john", ret)


@skip("Save for a future Sprint")
class TestTAEditPersonalInfo(BaseCase):
    # AT for PBI: As a TA, I want to be able to edit my own contact information

    def testTAEditPersonalInfo(self):
        #Assume ian is a TA
        self.cmd.callCommand("login ian TA")

        ret = self.cmd.callCommand("editAccount ian")
        self.assertEqual(ret, "Account ian successfully modified")
        ret = self.cmd.callCommand("viewAccount ian")
        #Assume ian changed his phone number to (414)555-5555
        self.assertIn("(414)555-5555", ret)


@skip("Save for a future Sprint")
class TestTAViewAssignments(BaseCase):
    # AT for PBI: As a TA, I want to be able to view TA assignments

    def testTAViewAssignments(self):
        #Assume ian is a TA
        self.cmd.callCommand("login ian TA")

        #Assume ian is assigned to course 01361 lab 01
        ret = self.cmd.callCommand("viewAssignmentTA ian")
        self.assertIn("Introduction to Software Engineering", ret)


class TestTAViewPublicInfo(BaseCase):
    # AT for PBI: As a TA, I want to be able to read the public contact information of all users

    def testTAViewPublicInfo(self):
        #Assume bob is a TA
        self.cmd.callCommand("login ian TA")

        #Assume instructor bill exists
        ret = self.cmd.callCommand("viewAccount bill")
        self.assertIn("bill", ret)
