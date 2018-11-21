from . import setup
from .cmd_interface import CmdInterface
from .file_io import FileIO
from ..models import Section


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

        temp = command_items.split("-")
        parent_courseID = temp[1]
        lecture_extension = temp[2]


    def validateInputParameters(self, parameters):
        # Need to check that the courseID is a 5 digit positive integer (> 99999)
        if len(parameters) != 2:
            return False

        return True
