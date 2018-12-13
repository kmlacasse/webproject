from .cmd_interface import CmdInterface
from ..models import Account
from .file_io import FileIO
from . import setup
from ..models import Account
from ..models import Course
from ..models import Section
from ..models import CourseMember
from ..models import SectionMember

class ViewInstructorAssignments(CmdInterface):

    def action(self, command_input):
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters."

        if setup.current_user is None:
            return "Failed. No user currently logged in."

        file = FileIO()
        instructor = file.readData(command_items[1], 'Account')
        if instructor is None:
            return "Failed. No such username."

        userPermissions = setup.current_user.permissions
        if (userPermissions[0] != '1' and userPermissions[1] != '1') or instructor.username == setup.current_user.username:
            return "Failed. Restricted action."

        if (instructor.permissions[2] == '0'):
            return "Failed. Username is not an instructor."

        sectionList = list(SectionMember.objects.filter(account__username=instructor.username))
        retString = ""
        for i in sectionList:
            section = file.readData(i.section.sectionID, 'Section')
            retString += (section.sectionID + "-" + section.sectionName + '\n')

        return retString


    def validateInputParameters(self, command_items):
        NUM_PARAMS = 2

        if len(command_items) == NUM_PARAMS:
            return True
        return False
