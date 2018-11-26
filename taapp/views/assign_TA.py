from .cmd_interface import CmdInterface
from ..models import Account
from .file_io import FileIO
from . import setup
from ..models import Account
from ..models import Course
from ..models import Section
from ..models import CourseMember
from ..models import SectionMember

class AssignTA(CmdInterface):

    def action(self, command_input):
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters."

        if setup.current_user is None:
            return "Failed. No user currently logged in."

        userPermissions = setup.current_user.permissions
        if userPermissions[0] != '1' and userPermissions[1] != '1':
            return "Failed. Restricted action."

        file = FileIO()
        TA = file.readData(command_items[1], 'Account')
        if TA is None:
            return "Failed. No such username."

        if (TA.permissions[3] == '0'):
            return "Failed. Username is not a TA."

        course = file.readData(command_items[2], 'Course')

        if course is None:
            return "Failed. Course does not exist."

        courseList = list(CourseMember.objects.filter(account__username=TA.username))
        for i in courseList:
            if(i.course.courseID == course.courseID):
                return TA.username + " already assigned to course."

        cMember = CourseMember.objects.create(account=TA, course=course)
        cMember.save()

        return TA.username + " successfully assigned to course."


    def validateInputParameters(self, command_items):
        NUM_PARAMS = 3

        if len(command_items) == NUM_PARAMS:
            return True
        return False
