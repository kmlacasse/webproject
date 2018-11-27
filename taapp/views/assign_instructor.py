from .cmd_interface import CmdInterface
from ..models import Account
from .file_io import FileIO
from . import setup
from ..models import Account
from ..models import Course
from ..models import Section
from ..models import CourseMember
from ..models import SectionMember


class AssignInstructor(CmdInterface):

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
        instructor = file.readData(command_items[1], 'Account')
        if instructor is None:
            return "Failed. No such username."

        if (instructor.permissions[2] == '0'):
            return "Failed. Username is not an instructor."

        lecture = file.readData(command_items[2], 'Section')

        if lecture is None:
            return "Failed. Course does not exist."

        sectMembers = SectionMember.objects.filter(section__sectionID=lecture.sectionID)
        if sectMembers.exists():
            return "Failed. Lecture already assigned an instructor."

        s = lecture.sectionID[:-1]
        course = file.readData(s, 'Course')

        cMember = CourseMember.objects.create(account=instructor, course=course)
        cMember.save()

        sMember = SectionMember.objects.create(account=instructor, section=lecture)
        sMember.save()

        return instructor.username + " successfully assigned to lecture."


    def validateInputParameters(self, command_items):
        NUM_PARAMS = 3

        if len(command_items) == NUM_PARAMS:
            return True
        return False
