from django.test import TestCase
from unittest import skip
from taapp.models import Account, Course, Section, CourseMember, SectionMember
from taapp.views import setup
from django.test import Client

""""
These are the Acceptance Tests for the TA Scheduling App for Team 404
"""


class BaseCase(TestCase):
    # Use this to setup tests for all cases
    def setUp(self):
        self.cmd = setup.setupCommands()
        setup.current_user = None
        self.c = Client()
        Account.objects.create(username="john", name="John", password="super", permissions="1000", email="john@uwm.edu", phone="41412344567", address="123 Cramer St., Milwaukee, WI  53211")
        Account.objects.create(username="rick", name="Rick", password="admin", permissions="0100", email="rick@uwm.edu", phone="2627654321", address="456 Kenwood Blvd., Milwaukee, WI  53211")
        Account.objects.create(username="bill", name="Bill", password="instructor", permissions="0010", email="bill@uwm.edu", phone="4140241357", address="789 Downer Ave., Milwaukee, WI  53211", officehours="Tuesday 5-6pm")
        Account.objects.create(username="ian", name="Ian", password="TA", permissions="0001", email="ian@uwm.edu", phone="4149756420", address="901 Newport Ave., Milwaukee, WI  53211", officehours="MW 11am - Noon")


class TestLogin(BaseCase):
    # AT for PBI 1:  As a user, I want to login through a webpage so I can issue commands

    def testLogin(self):
        # John has a supervisor account
        # John logs in
        ret = self.c.post('http://127.0.0.1:8000/login.html', {'username': 'john', 'password': 'super'})
        self.assertIn(b"john logged in", ret.content)
        # Try logging in again to verify that it is not possible because you are already logged in
        ret = self.c.post('http://127.0.0.1:8000/login.html', {'username': 'john', 'password': 'super'})
        self.assertIn(b"Failed. User currently logged in", ret.content)


class TestLogout(BaseCase):
    # AT for PBI 2:  As a user, I want to logout through a webpage so others don't issue commands as me

    def testLogout(self):
        # John has a supervisor account
        # John logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'john', 'password': 'super'})
        # John logs out
        ret = self.c.post('http://127.0.0.1:8000/logout.html')
        self.assertIn(b"Goodbye", ret.content)
        # Try to issue a command to verify that John is logged out
        ret = self.c.post('http://127.0.0.1:8000/logout.html')
        self.assertIn(b"Failed. No user currently logged in", ret.content)


class TestSupervisorCreateCourse(BaseCase):
    # AT for PBI 3:  As a Supervisor, I want to create a course through a webpage

    def tearDown(self):
        # Remove the created course
        self.cmd.callCommand("deleteCourse 01361")

    def testSupervisorCreateCourse(self):
        # John has a supervisor account
        # John logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'john', 'password': 'super'})
        # John creates a course which does not yet exist
        ret = self.c.post('http://127.0.0.1:8000/create_course.html', {'courseSub':'01', 'courseNum': '361', 'lectureNum':'1', 'labNum':'3', 'courseName': 'Introduction to Software Engineering'})
        self.assertIn(b"Course Introduction to Software Engineering  successfully added", ret.content)
        # Verify course was created by viewing it
        ret = self.c.post('http://127.0.0.1:8000/view_course.html', {'courseid': '01361'})
        self.assertIn(b"Introduction to Software Engineering", ret.content)


class TestSupervisorDeleteCourse(BaseCase):
    # AT for PBI 4:  As a Supervisor, I want to delete a course through a webpage

    def testSupervisorDeleteCourse(self):
        # John has a supervisor account
        # John logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'john', 'password': 'super'})
        # John creates a course which will be deleted
        ret = self.c.post('http://127.0.0.1:8000/create_course.html',{'courseSub': '01', 'courseNum': '361', 'lectureNum': '1', 'labNum': '3','courseName': 'Introduction to Software Engineering'})
        # John deletes the course
        ret = self.c.post('http://127.0.0.1:8000/delete_course.html', {'courseid':'01361'})
        self.assertIn(b"Course 01361 successfully removed.", ret.content)


class TestSupervisorCreateAccount(BaseCase):
    # AT for PBI 5:  As a Supervisor, I want to create an account through a webpage

    def tearDown(self):
        # Remove the created account
        self.cmd.callCommand("deleteAccount tim")

    def testSupervisorCreateAccount(self):
        # John has a supervisor account
        # John logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'john', 'password': 'super'})
        # John creates an account which does not yet exist
        ret = self.c.post('http://127.0.0.1:8000/create_account.html', {'username': 'tim', 'password':'default','role':'supervisor'})
        self.assertIn(b"Account tim successfully added", ret.content)
        # Login to new account to verify that it was created
        self.c.post('http://127.0.0.1:8000/logout.html')
        ret = self.c.post('http://127.0.0.1:8000/login.html', {'username': 'tim', 'password': 'default'})
        self.assertIn(b"tim logged in", ret.content)


class TestSupervisorDeleteAccount(BaseCase):
    # AT for PBI 6:  As a Supervisor, I want to delete an account through a webpage

    def testSupervisorDeleteAccount(self):
        # John has a supervisor account
        # John logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'john', 'password': 'super'})
        # John creates an account which does not yet exist
        ret = self.c.post('http://127.0.0.1:8000/create_account.html', {'username': 'tim', 'password':'default','role':'supervisor'})
        self.assertIn(b"Account tim successfully added", ret.content)
        # John deletes the account
        ret = self.c.post('http://127.0.0.1:8000/delete_account.html', {'username': 'tim'})
        self.assertIn(b"Account tim successfully removed.", ret.content)
        # Try to login to account to verify that it does not exist
        self.c.post('http://127.0.0.1:8000/logout.html')
        ret = self.c.post('http://127.0.0.1:8000/login.html', {'username': 'tim', 'password': 'default'})
        self.assertIn(b"Failed. No such username", ret.content)


@skip("Save for a future Sprint")
class TestSupervisorEditAccount(BaseCase):
    # AT for PBI 7:  As a Supervisor, I want to edit an account through a webpage

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


class TestSupervisorViewSectionsCourse(BaseCase):
    # AT for PBI 8:  As a supervisor, I want to see the number of sections per course through a webpage,
    # to determine the minimum number of instructors to assign

    def tearDown(self):
        # Remove the created course
        self.cmd.callCommand("deleteCourse 01361")

    def testSupervisorViewSectionsCourse(self):
        # John has a supervisor account
        # John logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'john', 'password': 'super'})
        # Create a course which will be viewed
        ret = self.c.post('http://127.0.0.1:8000/create_course.html',
                          {'courseSub': '01', 'courseNum': '361', 'lectureNum': '1', 'labNum': '3',
                           'courseName': 'Introduction to Software Engineering'})
        # John views a course which exists
        ret = self.c.post('http://127.0.0.1:8000/view_course.html', {'courseid': '01361'})
        self.assertIn(b"1", ret.content)


class TestSupervisorViewLabsCourse(BaseCase):
    # Also AT for PBI 9:  As a supervisor, I would like to be able to see the number of lab sections
    # through a webpage, so that I know the minimum number of TAs required

    def tearDown(self):
        # Remove the created course
        self.cmd.callCommand("deleteCourse 01361")

    def testSupervisorViewLabsCourse(self):
        # John has a supervisor account
        # John logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'john', 'password': 'super'})
        # Create a course which will be viewed
        ret = self.c.post('http://127.0.0.1:8000/create_course.html',
                          {'courseSub': '01', 'courseNum': '361', 'lectureNum': '1', 'labNum': '3',
                           'courseName': 'Introduction to Software Engineering'})
        # John views a course which exists
        ret = self.c.post('http://127.0.0.1:8000/view_course.html', {'courseid': '01361'})
        self.assertIn(b"3", ret.content)


class TestSupervisorAssignTAtoCourse(BaseCase):
    # AT for PBI 10:  As a supervisor, I would like to be able to assign TAs to courses through a webpage,
    # so that each course would have sufficient number of TAs

    def tearDown(self):
        # Delete the course and TA created
        self.cmd.callCommand("deleteCourse 01361")
        self.cmd.callCommand("deleteAccount ian")

    def testSupervisorAssignTAtoCourse(self):
        # John logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'john', 'password': 'super'})
        # Create a course
        ret = self.c.post('http://127.0.0.1:8000/create_course.html',
                          {'courseSub': '01', 'courseNum': '361', 'lectureNum': '1', 'labNum': '3',
                           'courseName': 'Introduction to Software Engineering'})
        # Create an instructor
        self.cmd.callCommand("createAccount tim default 0010")
        # John assigns an instructor to a course
        ret = self.c.post('http://127.0.0.1:8000/assign_instructor.html',
                          {'username': 'tim', 'courseID': '01361', 'lecture': '1'})
        self.assertIn(b"tim successfully assigned", ret.content)
        # Create a TA
        self.c.post('http://127.0.0.1:8000/create_account.html',
                          {'username': 'logan', 'password': 'pass123', 'role': 'ta'})
        # John assigns a TA to a course
        self.c.post('http://127.0.0.1:8000/assign_TA.html', {'username':'logan', 'courseID':'01361'})


class TestSupervisorAssignTAtoLab(BaseCase):
    # AT for PBI 11:  As a supervisor, I would like to be able to assign TAs to specific lab sections
    # through a webpage, so that TAs can work around their schedule

    def tearDown(self):
        # Delete the course and TA created
        self.cmd.callCommand("deleteCourse 01361")
        self.cmd.callCommand("deleteAccount ian")

    def testSupervisorAssignTAtoLab(self):
        # John logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'john', 'password': 'super'})
        # Create a course
        ret = self.c.post('http://127.0.0.1:8000/create_course.html',
                          {'courseSub': '01', 'courseNum': '361', 'lectureNum': '1', 'labNum': '3',
                           'courseName': 'Introduction to Software Engineering'})
        # Create an instructor
        self.cmd.callCommand("createAccount tim default 0010")
        # John assigns an instructor to a course
        ret = self.c.post('http://127.0.0.1:8000/assign_instructor.html',
                          {'username': 'tim', 'courseID': '01361', 'lecture': '1'})
        self.assertIn(b"tim successfully assigned", ret.content)
        # Create a TA
        self.c.post('http://127.0.0.1:8000/create_account.html', {'username': 'logan', 'password': 'pass123', 'role': 'ta'})
        # John assigns a TA to a course
        self.c.post('http://127.0.0.1:8000/assign_TA.html', {'username':'logan', 'courseID':'01361'})
        # John assigns a TA to a lab section
        ret = self.c.post('http://127.0.0.1:8000/assign_TA_to_lab.html', {'username': 'logan', 'courseID': '01361', 'lab':'101'})
        self.assertIn(b"successfully assigned", ret.content)


class TestSupervisorAssignInstructortoCourse(BaseCase):
    # AT for PBI 12:  As a supervisor, I want to assign an instructor to a course through a webpage

    def tearDown(self):
        # Delete the course and instructor created
        self.cmd.callCommand("deleteCourse 01361")
        self.cmd.callCommand("deleteAccount tim")

    def testSupervisorAssignTAtoLab(self):
        # John has a supervisor account
        # John logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'john', 'password': 'super'})
        # Create a course
        ret = self.c.post('http://127.0.0.1:8000/create_course.html',
                          {'courseSub': '01', 'courseNum': '361', 'lectureNum': '1', 'labNum': '3',
                           'courseName': 'Introduction to Software Engineering'})
        # Create an instructor
        self.cmd.callCommand("createAccount tim default 0010")
        # John assigns an instructor to a course
        ret = self.c.post('http://127.0.0.1:8000/assign_instructor.html', {'username': 'tim', 'courseID': '01361', 'lecture':'1'})
        self.assertIn(b"tim successfully assigned", ret.content)


class TestAdministratorCreateCourse(BaseCase):
    # AT for PBI 13:  As an administrator, I want to create a course through a webpage

    def tearDown(self):
        # Remove the created course
        self.cmd.callCommand("deleteCourse 01361")

    def testAdministratorCreateCourse(self):
        # Rick has an administrator account
        # Rick logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'rick', 'password': 'admin'})
        # Rick creates a course which does not yet exist
        ret = self.c.post('http://127.0.0.1:8000/create_course.html', {'courseSub':'01', 'courseNum': '361', 'lectureNum':'1', 'labNum':'3', 'courseName': 'Introduction to Software Engineering'})
        self.assertIn(b"Course Introduction to Software Engineering  successfully added", ret.content)
        # Verify course was created by viewing it
        ret = self.c.post('http://127.0.0.1:8000/view_course.html', {'courseid': '01361'})
        self.assertIn(b"Introduction to Software Engineering", ret.content)


class TestAdministratorDeleteCourse(BaseCase):
    # AT for PBI 14:  As an administrator, I want to delete a course through a webpage

    def testAdministratorDeleteCourse(self):
        # Rick has an administrator account
        # John logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'rick', 'password': 'admin'})
        # John creates a course which will be deleted
        ret = self.c.post('http://127.0.0.1:8000/create_course.html',{'courseSub': '01', 'courseNum': '361', 'lectureNum': '1', 'labNum': '3','courseName': 'Introduction to Software Engineering'})
        # John deletes the course
        ret = self.c.post('http://127.0.0.1:8000/delete_course.html', {'courseid':'01361'})
        self.assertIn(b"Course 01361 successfully removed.", ret.content)


class TestAdministratorCreateAccount(BaseCase):
    # AT for PBI 15:  As an administrator, I want to create an account through a webpage

    def tearDown(self):
        # Remove the created account
        self.cmd.callCommand("deleteAccount tim")

    def testAdministratorCreateAccount(self):
        # Rick has an administrator account
        # Rick logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'rick', 'password': 'admin'})
        # Rick creates an account which does not yet exist
        ret = self.c.post('http://127.0.0.1:8000/create_account.html', {'username': 'tim', 'password':'default','role':'supervisor'})
        self.assertIn(b"Account tim successfully added", ret.content)
        # Login to new account to verify that it was created
        self.c.post('http://127.0.0.1:8000/logout.html')
        ret = self.c.post('http://127.0.0.1:8000/login.html', {'username': 'tim', 'password': 'default'})
        self.assertIn(b"tim logged in", ret.content)


class TestAdministratorDeleteAccount(BaseCase):
    # AT for PBI 16:  As an administrator, I want to delete an account through a webpage

    def testAdministratorDeleteAccount(self):
        # Rick has an administrator account
        # Rick logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'rick', 'password': 'admin'})
        # Rick creates an account which does not yet exist
        ret = self.c.post('http://127.0.0.1:8000/create_account.html', {'username': 'tim', 'password':'default','role':'supervisor'})
        self.assertIn(b"Account tim successfully added", ret.content)
        # Rick deletes the account
        ret = self.c.post('http://127.0.0.1:8000/delete_account.html', {'username': 'tim'})
        self.assertIn(b"Account tim successfully removed.", ret.content)
        # Try to login to account to verify that it does not exist
        self.c.post('http://127.0.0.1:8000/logout.html')
        ret = self.c.post('http://127.0.0.1:8000/login.html', {'username': 'tim', 'password': 'default'})
        self.assertIn(b"Failed. No such username", ret.content)


@skip("Save for a future Sprint")
class TestAdministratorEditAccount(BaseCase):
    # AT for PBI 17:  As an administrator, I want to edit an account through a webpage

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
class TestInstructorViewTA(BaseCase):
    # AT for PBI 18: As an instructor, I want to view the TAs assigned to my courses through a webpage

    def testInstructorViewTA(self):
        # Assume Bill is an Instructor
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
    # At for PBI 19: As an Instructor, I want to edit my personal contact information through a webpage

    def testInstructorEditPersonalInfo(self):
        # Assume Bill is an Instructor
        # Bill logs in
        self.cmd.callCommand("login bill instructor")

        ret = self.cmd.callCommand("editAccount bill")
        self.assertEqual("Account bill successfully modified", ret)
        ret = self.cmd.callCommand("viewAccount bill")
        # Assuming bill changed his phone number to (414)555-5555
        self.assertIn("(414)555-5555", ret)


class TestInstructorViewAssignmentInstructor(BaseCase):
    # AT for PBI 20: As an instructor, I want to view the courses I am assigned to through a webpage

    def testInstructorViewAssignmentInstructor(self):
        # John logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'john', 'password': 'super'})
        # Create a course
        ret = self.c.post('http://127.0.0.1:8000/create_course.html',
                          {'courseSub': '01', 'courseNum': '361', 'lectureNum': '1', 'labNum': '3',
                           'courseName': 'Introduction to Software Engineering'})
        # Create an instructor
        self.cmd.callCommand("createAccount tim default 0010")
        # John assigns an instructor to a course
        ret = self.c.post('http://127.0.0.1:8000/assign_instructor.html',
                          {'username': 'tim', 'courseID': '01361', 'lecture': '1'})
        self.assertIn(b"tim successfully assigned", ret.content)
        # Tim logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'tim', 'password': 'default'})
        # Assume bill is already assigned to class 01361
        ret = self.c.post('http://127.0.0.1:8000/view_instructor_assignments.html', {'username': 'tim'})
        self.assertIn(b"Introduction to Software Engineering", ret.content)


class TestInstructorAssignTAtoLab(BaseCase):
    # AT for PBI 21: As an Instructor, I want to be able to assign my TAS to particular lab sections through a webpage

    def tearDown(self):
        # Remove the created and modified account
        self.cmd.callCommand("deleteAccount nate")
        self.cmd.callCommand("deleteCourse 01361")

    def testInstructorAssignTAtoLab(self):
        # John logs in
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'john', 'password': 'super'})
        # Create a course
        ret = self.c.post('http://127.0.0.1:8000/create_course.html',
                          {'courseSub': '01', 'courseNum': '361', 'lectureNum': '1', 'labNum': '3',
                           'courseName': 'Introduction to Software Engineering'})
        # Create an instructor
        self.cmd.callCommand("createAccount tim default 0010")
        # John assigns an instructor to a course
        ret = self.c.post('http://127.0.0.1:8000/assign_instructor.html',
                          {'username': 'tim', 'courseID': '01361', 'lecture': '1'})
        self.assertIn(b"tim successfully assigned", ret.content)
        # Create a TA
        self.c.post('http://127.0.0.1:8000/create_account.html',
                    {'username': 'nate', 'password': 'pass123', 'role': 'ta'})
        # John assigns a TA to a course
        ret = self.c.post('http://127.0.0.1:8000/assign_TA.html', {'username': 'nate', 'courseID': '01361'})
        self.assertIn(b"nate successfully assigned", ret.content)
        # Assume Tim is an Instructor
        self.c.post('http://127.0.0.1:8000/logout.html')
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'tim', 'password': 'default'})
        # Assume TA Nate is assigned to course 01361
        ret = self.c.post('http://127.0.0.1:8000/assign_TA_to_lab.html', {'username': 'nate', 'courseID':'01361', 'lab':'102'})
        self.assertIn(b"successfully assigned", ret.content)


class TestInstructorViewPublicInfo(BaseCase):
    # AT for PBI 22: As an instructor, I want to be able to read public contact information
    # of all users through a webpage

    def testInstructorViewPublicInfo(self):
        # Assume Bill is an Instructor
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'bill', 'password': 'instructor'})

        # Assume TA ian and Supervisor john exists
        ret = self.c.post('http://127.0.0.1:8000/view_account.html', {'name': 'ian'})
        self.assertIn(b"ian", ret.content)
        ret = self.c.post('http://127.0.0.1:8000/view_account.html', {'name': 'john'})
        self.assertIn(b"john", ret.content)


@skip("Save for a future Sprint")
class TestTAEditPersonalInfo(BaseCase):
    # AT for PBI 23: As a TA, I want to be able to edit my own contact information through a webpage

    def testTAEditPersonalInfo(self):
        # Assume ian is a TA
        self.cmd.callCommand("login ian TA")

        ret = self.cmd.callCommand("editAccount ian")
        self.assertEqual(ret, "Account ian successfully modified")
        ret = self.cmd.callCommand("viewAccount ian")
        # Assume ian changed his phone number to (414)555-5555
        self.assertIn("(414)555-5555", ret)


@skip("Waiting to implement")
class TestTAViewAssignments(BaseCase):
    # AT for PBI 24: As a TA, I want to be able to view TA assignments through a webpage

    def testTAViewAssignments(self):
        # Assume ian is a TA
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'ian', 'password': 'TA'})

        # Assume ian is assigned to course 01361 lab 01
        ret = self.c.post('http://127.0.0.1:8000/view_TA_assignments.html', {'username': 'ian'})
        self.assertIn(b"Introduction to Software Engineering", ret.content)

class TestTAViewPublicInfo(BaseCase):
    # AT for PBI 25: As a TA, I want to be able to read the public contact information of all users
    # through a webpage

    def testTAViewPublicInfo(self):
        # Assume bob is a TA
        self.c.post('http://127.0.0.1:8000/login.html', {'username': 'ian', 'password': 'TA'})

        # Assume instructor bill exists
        ret = self.c.post('http://127.0.0.1:8000/view_account.html', {'name': 'bill'})
        self.assertIn(b"bill", ret.content)


class TestAccessWebsite(BaseCase):
    # AT for PBI 26: As a visitor, I can access the homepage

    def testAccessWebsite(self):
        response = self.client.get("http://127.0.0.1:8000/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')


class TestUserLogin(BaseCase):
    # AT for PBI 27: As a user, I can login through the webpage

    def testUserLogin(self):
        # Ian logs in as a TA
        ret = self.cmd.callCommand("login ian TA")
        self.assertEqual(ret, "ian logged in")
        # Try logging in again to verify that it is not possible because you are already logged in
        ret = self.cmd.callCommand("login ian TA")
        self.assertEqual(ret, "Failed. User currently logged in")

