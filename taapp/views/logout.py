from .cmd_interface import CmdInterface
from . import setup as setup


class Logout(CmdInterface):

    def action(self, command_input):
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters"

        if setup.current_user is None:
            return "Failed. No current user to log out"

        setup.current_user = None

        return "Goodbye"

    def validateInputParameters(self, command_items):
        NUM_PARAMS = 1

        if len(command_items) == NUM_PARAMS:
            return True
        return False
