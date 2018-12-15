from . import setup
from .cmd_interface import CmdInterface
from .file_io import FileIO
from ..models import Account
from ..models import Section
from ..models import SectionMember

#viewLecture(01361-1)
class ViewLecture(CmdInterface):
    def action(self, command_input):

        # Checks that there is user currently logged in
        if setup.current_user is None:
            return "Failed. No user currently logged in"

        # Verify legal parameters
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)
        if not valid_params:
            return "Failed. Invalid parameters"

        file = FileIO()
        section_data = file.readData(command_items[1], 'Section')
        if section_data is None:
            return "Failed. Lecture section does not exist"

        instructor_name = ""
        section_member = file.readData(section_data.sectionID, 'SectionMember')
        if section_member is not None:
            # Means that there is an instructor assigned to the lecture
            instructor_name += section_member.account__name


        ret_str = "Lecture ID: " + command_items[1] + '   ' + "Section Name: " + section_data.sectionName + '  ' +  "Instructor: " + instructor_name
        return ret_str

    def validateInputParameters(self, parameters):
        if len(parameters) != 2:
            return False

        return True
