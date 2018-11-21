from . import setup as setup
from .cmd_interface import CmdInterface
from .file_io import FileIO
from ..models import Account


class Login(CmdInterface):

    def action(self, command_input):

        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters"

        if setup.current_user is not None:
            return "Failed. User currently logged in"

        file = FileIO()
        user = file.readData(command_items[1], "Account")

        if user is None:
            return "Failed. No such username"

        if command_items[2] != user.password:
            return "Failed. Username or password invalid"

        setup.current_user = user
        return user.username + " logged in"

    def validateInputParameters(self, command_items):
        NUM_PARAMS = 3

        if len(command_items) == NUM_PARAMS:
            return True
        return False
