from .cmd_interface import CmdInterface
from .file_io import FileIO
from . import setup


class DeleteCourse(CmdInterface):

    def action(self, command_input):
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters"

        if setup.current_user is None:
            return "Failed. No user currently logged in"

        userPermissions = setup.current_user.permissions
        if userPermissions[0] != '1' and userPermissions[1] != '1':
            return "Failed. Restricted action."

        file = FileIO()
        lectures = file.readData(command_items[1], 'Course')

        if lectures == None:
            return "Failed. Course " + command_items[1] + " doesn't exist."
        else:
            exists = file.deleteData(command_items[1], 'Course')
            return "Course " + command_items[1] + " successfully removed."

    def validateInputParameters(self, command_items):
        if len(command_items) != 2:
            return False
        return True
