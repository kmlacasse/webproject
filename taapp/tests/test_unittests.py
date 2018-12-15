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
        setup.current_user = None
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
        self.assertEqual(ret, "Failed. Username is not a TA.")

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

        # assign ian to course 01361
        ret = self.cmd.callCommand("assignTA ian 01361")
        self.assertEqual(ret, "ian successfully assigned to course.")

        #assign ian to lab 01361101
        ret = self.cmd.callCommand("assignTAtoLab ian 01361101")
        self.assertEqual(ret, "Ian successfully assigned to lab.")

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
        self.assertEqual(ret, "Failed. Username is not a TA.")

        #course does not exist
        ret = self.cmd.callCommand("assignTAtoLab ian 00000000")
        self.assertEqual(ret, "Failed. TA is not assigned to course.")

        #logout super
        self.cmd.callCommand("logout")

        #login non super
        self.cmd.callCommand("login ian TA")

        #attempt to assignTAtoLab
        ret = self.cmd.callCommand("assignTAtoLab ian 01361101")
        self.assertEqual(ret, "Failed. Restricted action.")


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
        self.assertIn("bill", ret)

        # Now Rick is logged in instead
        setup.current_user = Account.objects.get(username="rick")

        # Bill views an account and can see the private information
        ret = self.cmd.callCommand("viewAccount john")
        self.assertIn("john", ret)

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


class TestEditAccount(BaseCase):

    # Unit Tests for the editAccount command

    def testEditAccountInvalid(self):
        # No user logged in
        setup.current_user = None

        # Attempt to change Bill's password
        ret = self.cmd.callCommand("editAccount bill password invalid")
        self.assertEqual(ret, "Failed. No user currently logged in")

        # Bill logs in
        setup.current_user = Account.objects.get(username="bill")

        # Bill enters invalid parameters
        ret = self.cmd.callCommand("editAccount bill")
        self.assertEqual(ret, "Failed. Invalid parameters")

        # Bill tries to edit John's password
        ret = self.cmd.callCommand("editAccount john password invalid")
        self.assertEqual(ret, "Failed. Restricted action")

        # Bill logs out and John logs in
        setup.current_user = Account.objects.get(username="john")

        # John tries to change Mike's password, Mike doesn't exist
        ret = self.cmd.callCommand("editAccount mike password invalid")
        self.assertEqual(ret, "Failed. Username doesn't exist")

    def testEditAccountValid(self):
        # Bill logs in
        setup.current_user = Account.objects.get(username="bill")

        # Bill changes his password
        ret = self.cmd.callCommand("editAccount bill password valid")
        self.assertEqual(ret, "Account bill successfully modified")

        # Bill logs out and John logs in
        setup.current_user = Account.objects.get(username="john")

        # John changes Bill's password back
        ret = self.cmd.callCommand("editAccount bill password instructor")
        self.assertEqual(ret, "Account bill successfully modified")


class TestViewUsers(BaseCase):

    # Unit Tests for the viewUsers command

    def testViewUsersInvalid(self):
        # John attempts to view users without being logged in
        ret = self.cmd.callCommand("viewUsers")
        self.assertEqual(ret, "Failed. No user currently logged in")

        # John is logged in
        setup.current_user = Account.objects.get(username="john")

        # John attempts to view users with too many parameters
        ret = self.cmd.callCommand("viewUsers extra")
        self.assertEqual(ret, "Failed. Invalid parameters")

    def testViewUsersValid(self):
        # John is logged in
        setup.current_user = Account.objects.get(username="john")

        # John views the users
        ret = self.cmd.callCommand("viewUsers")
        self.assertIn("john", ret[0])
        self.assertIn("rick", ret[1])
        self.assertIn("bill", ret[2])
        self.assertIn("ian", ret[3])


class TestCreateCourse(BaseCase):
    def testSupervisorCreateCourse(self):
        # John logs in with a supervisor account
        setup.current_user = Account.objects.get(username="john")

        # John creates a course which does not yet exist
        ret = self.cmd.callCommand("createCourse 02150 1 1 Intro to Electrical Engineering")
        self.assertEqual(ret, "Course Intro to Electrical Engineering  successfully added")

        # John attempts to duplicate the course
        ret = self.cmd.callCommand("createCourse 02150 1 1 Intro to Electrical Engineering")
        self.assertEqual(ret, "Failed. Course already exists")

        # John logs out
        setup.current_user = None

    def testAdministratorCreateCourse(self):
        # Rick logs in with a administrator account
        setup.current_user = Account.objects.get(username="rick")

        # Rick creates a course which does not yet exist
        ret = self.cmd.callCommand("createCourse 02150 1 1 Intro to Electrical Engineering")
        self.assertEqual(ret, "Course Intro to Electrical Engineering  successfully added")

        # Rick logs out
        setup.current_user = None

    def testInstructorCreateCourse(self):
        # Bill logs into an instructor account
        setup.current_user = Account.objects.get(username="bill")

        # Bill attempts to create a course
        ret = self.cmd.callCommand("createCourse 02150 1 1 Intro to Electrical Engineering")
        self.assertEqual(ret, "Failed. Restricted action")

        # Bill logs out
        setup.current_user = None

    def testTACreateCourse(self):
        # Ian logs into a TA account
        setup.current_user = Account.objects.get(username="ian")

        # Ian attempts to create a course
        ret = self.cmd.callCommand("createCourse 02150 1 1 Intro to Electrical Engineering")
        self.assertEqual(ret, "Failed. Restricted action")

        # Ian logs out
        setup.current_user = None

    def testNoUserCreateCourse(self):
        # Nobody logged in, attempt to create a course
        ret = self.cmd.callCommand("createCourse 02150 1 1 Intro to Electrical Engineering")
        self.assertEqual(ret, "Failed. No user currently logged in")

    def testInvalidParametersCreateCourse(self):
        # John logs in with supervisor account
        setup.current_user = Account.objects.get(username="john")

        # Invalid lecture count
        ret = self.cmd.callCommand("createCourse 02150 0 1 Intro to Electrical Engineering")
        self.assertEqual(ret, "Failed. Invalid parameters")

        # Invalid lab count
        ret = self.cmd.callCommand("createCourse 02150 1 -1 Intro to Electrical Engineering")
        self.assertEqual(ret, "Failed. Invalid parameters")

        #John logs out
        setup.current_user = None


class TestViewCourse(BaseCase):
    def testViewCourseValid(self):
        # John logs in
        setup.current_user = Account.objects.get(username="john")

        # John views the course
        ret = self.cmd.callCommand("viewCourse 01361")
        self.assertIn("Introduction to Software Engineering", ret)

        #John logs out
        setup.current_user = None

    def testViewCourseInvalid(self):
        # No user logged in attempts to view course
        ret = self.cmd.callCommand("viewCourse 01361")
        self.assertEqual(ret, "Failed. No user currently logged in")

        # John logs in
        setup.current_user = Account.objects.get(username="john")

        # John attempts to view non existing course
        ret = self.cmd.callCommand("viewCourse 02300")
        self.assertEqual(ret, "Failed. Course does not exists")

        # John logs out
        setup.current_user = None

class TestDeleteAccount(BaseCase):

    def testDeleteAccountNoUser(self):


        #login in as anyone, using john
        self.cmd.callCommand("login john super")

        #Let's try to delete an account that doesn't exist
        retString = self.cmd.callCommand("deleteAccount joseph")
        self.assertEqual(retString, "Failed. Username doesn't exist.")

        #LOGGING OUT
        self.cmd.callCommand("logout")

    def testDeleteAccountTA(self):


        #still logged in as john but we will test to make sure that readding data should return None as specified.
        self.cmd.callCommand("login ian TA")

        retString = self.cmd.callCommand("deleteAccount john")
        #jerry cannot access it because hes a damn ta. who does he think he is!?
        self.assertEqual(retString, "Failed. Restricted action.")

        self.cmd.callCommand("logout")

    def testDeleteAccountInstructor(self):


        #still logged in as john but we will test to make sure that readding data should return None as specified.
        self.cmd.callCommand("login bill instructor")

        retString = self.cmd.callCommand("deleteAccount john")
        #jerry cannot access it because hes a damn ta. who does he think he is!?
        self.assertEqual(retString, "Failed. Restricted action.")

        self.cmd.callCommand("logout")

    def testDeleteAccountSupervisor(self):
        #login as super John


        self.cmd.callCommand("login john super")

        retString = self.cmd.callCommand("deleteAccount ian")
        self.assertEqual(retString, "Account ian successfully removed.")
        self.cmd.callCommand("logout")

    def testDeleteAccountAdministrator(self):


        self.cmd.callCommand("login rick admin")
        retString = self.cmd.callCommand("deleteAccount ian")
        self.assertEqual(retString, "Account ian successfully removed.")
        self.cmd.callCommand("logout")

    def testDeleteAccountCurrent(self):


        self.cmd.callCommand("login john super")
        retString = self.cmd.callCommand("deleteAccount john")

        self.assertEqual(retString, "Failed. Cannot delete logged in account.")

        self.cmd.callCommand("Failed. Cannot delete logged in account.")

        self.cmd.callCommand("logout")


class TestDeleteCourse(BaseCase):

    def testTestDeleteCourseTA(self):

        #still logged in as john but we will test to make sure that readding data should return None as specified.
        self.cmd.callCommand("login ian TA")

        retString = self.cmd.callCommand("deleteCourse 01361")
        #jerry cannot access it because hes a damn ta. who does he think he is!?
        self.assertEqual(retString, "Failed. Restricted action.")

        self.cmd.callCommand("logout")

    def testDeleteCourseInstructor(self):


        #still logged in as john but we will test to make sure that readding data should return None as specified.
        self.cmd.callCommand("login bill instructor")

        retString = self.cmd.callCommand("deleteCourse 01361")
        #jerry cannot access it because hes a damn ta. who does he think he is!?
        self.assertEqual(retString, "Failed. Restricted action.")

        self.cmd.callCommand("logout")

    def testDeleteCourseSupervisor(self):


        #login as super John
        self.cmd.callCommand("login john super")

        retString = self.cmd.callCommand("deleteCourse 01361")
        self.assertEqual(retString, "Course 01361 successfully removed.")
        self.cmd.callCommand("logout")

    def testDeleteCourseAdministrator(self):


        self.cmd.callCommand("login rick admin")
        retString = self.cmd.callCommand("deleteCourse 01361")
        self.assertEqual(retString, "Course 01361 successfully removed.")
        self.cmd.callCommand("logout")

    def testDeleteCourseNoCourse(self):


        #login in as anyone, using john
        self.cmd.callCommand("login john super")

        #Let's try to delete an account that doesn't exist
        retString = self.cmd.callCommand("deleteCourse 013619")
        self.assertEqual(retString, "Failed. Course 013619 doesn't exist.")

        #LOGGING OUT
        self.cmd.callCommand("logout")

class TestViewInstructorAssignments(BaseCase):

    # Unit Tests for viewInstructorAssignments command

    def testViewInstructorAssignmentsSuccessAndDup(self):
        #login super
        self.cmd.callCommand("login john super")

        #assign bill to lecture 013611
        self.cmd.callCommand("assignInstructor bill 013611")

        #view bill's assignments
        ret = self.cmd.callCommand("viewInstructorAssignments bill")
        self.assertIn("013611", ret[0])

        #logout
        self.cmd.callCommand("logout")

        #login bill
        self.cmd.callCommand("login bill instructor")

        #view bill's assignments as bill
        ret = self.cmd.callCommand("viewInstructorAssignments bill")
        self.assertIn("013611", ret[0])

    def testViewInstructorAssignmentsInvalid(self):
        #no user logged in
        ret = self.cmd.callCommand("viewInstructorAssignments bill")
        self.assertEqual(ret, "Failed. No user currently logged in.")

        #login super
        self.cmd.callCommand("login john super")

        #invalid parameters
        ret = self.cmd.callCommand("viewInstructorAssignments ")
        self.assertEqual(ret, "Failed. Invalid parameters.")

        #No such user
        ret = self.cmd.callCommand("viewInstructorAssignments xyz")
        self.assertEqual(ret, "Failed. No such username.")

        #username is not an instructor
        ret = self.cmd.callCommand("viewInstructorAssignments rick")
        self.assertEqual(ret, "Failed. Username is not an instructor.")

        #logout super
        self.cmd.callCommand("logout")

        #login non super and not bill
        self.cmd.callCommand("login ian TA")

        #attempt to assigninstructor
        ret = self.cmd.callCommand("viewInstructorAssignments bill")
        self.assertEqual(ret, "Failed. Restricted action.")

class TestViewTAAssignments(BaseCase):

    # Unit Tests for viewTAAssignments command

    def testViewTAAssignmentsSuccessAndDup(self):
        #login super
        self.cmd.callCommand("login john super")

        #assign ian to course 01361
        self.cmd.callCommand("assignTA ian 01361")

        #assign ian to lab 01361101
        self.cmd.callCommand("assignTAtoLab ian 01361101")

        #view ian's assignments
        ret = self.cmd.callCommand("viewTAAssignments ian")
        self.assertIn("01361101", ret[0])

        #logout
        self.cmd.callCommand("logout")

        #login ian
        self.cmd.callCommand("login ian TA")

        #view ian's assignments as ian
        ret = self.cmd.callCommand("viewTAAssignments ian")
        self.assertIn("01361101", ret[0])

    def testViewTAAssignmentsInvalid(self):
        #no user logged in
        ret = self.cmd.callCommand("viewTAAssignments ian")
        self.assertEqual(ret, "Failed. No user currently logged in.")

        #login super
        self.cmd.callCommand("login john super")

        #invalid parameters
        ret = self.cmd.callCommand("viewTAAssignments ")
        self.assertEqual(ret, "Failed. Invalid parameters.")

        #No such user
        ret = self.cmd.callCommand("viewTAAssignments xyz")
        self.assertEqual(ret, "Failed. No such username.")

        #username is not an instructor
        ret = self.cmd.callCommand("viewTAAssignments bill")
        self.assertEqual(ret, "Failed. Username is not a TA.")

        #logout super
        self.cmd.callCommand("logout")

        #login non super and not ian
        self.cmd.callCommand("login bill instructor")

        #attempt to assigninstructor
        ret = self.cmd.callCommand("viewTAAssignments ian")
        self.assertEqual(ret, "Failed. Restricted action.")
