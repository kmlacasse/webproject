from .cmd_interface import CmdInterface
from ..models import Account
from .file_io import FileIO
from . import setup


class CreateAccount(CmdInterface):

    def action(self, command_input):
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters"

        if setup.current_user is None:
            return "Failed. No user currently logged in"

        current_user_permissions = setup.current_user.permissions
        if current_user_permissions[0] != '1' and current_user_permissions[1] != '1':
            return "Failed. Restricted action"

        file = FileIO()
        user_check = file.readData(command_items[1], 'Account')
        if user_check is not None:
            return "Failed. Username currently in use"

        new_user = Account.objects.create(username=command_items[1], password=command_items[2], permissions=command_items[3])
        new_user.save()

        return "Account " + new_user.username + " successfully added"

    def validateInputParameters(self, command_items):
        if len(command_items) != 4:
            return False

        for i in range(4):
            if command_items[3][i] is not '0' and command_items[3][i] is not '1':
                return False

        return True
