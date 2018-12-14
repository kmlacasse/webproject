from . import setup
from .cmd_interface import CmdInterface
from .file_io import FileIO


class ViewAccount(CmdInterface):

    def action(self, command_input):

        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters"

        if setup.current_user is None:
            return "Failed. No user currently logged in"

        # Get information for the account being viewed
        file = FileIO()
        person = file.readData(command_items[1], "Account")

        if person is None:
            return "Failed. No account " + command_items[1]

        # Supervisors and admins can view all data
        if setup.current_user.permissions[0] == '1' or setup.current_user.permissions[1] == '1':
            ret = self.displayAllInfo(person)
        # Individuals can also view all of their own data
        elif setup.current_user.username == command_items[1]:
            ret = self.displayAllInfo(person)
        # Everyone can view public data of anyone
        else:
            ret = self.displayPublicInfo(person)
        return ret

    def validateInputParameters(self, command_items):
        NUM_PARAMS = 2

        if len(command_items) == NUM_PARAMS:
            return True
        return False

    def displayAllInfo(self, person):
        ret = [person.username, person.name, person.email, person.officehours, person.phone, person.address]
        return ret

    def displayPublicInfo(self, person):
        ret = [person.username, person.name, person.email, person.officehours]
        return ret
