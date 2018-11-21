from .cmd_interface import CmdInterface
from .file_io import FileIO
from . import setup


class DeleteAccount(CmdInterface):

    def action(self, command_input):
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters"

        if setup.current_user is None:
            return "Failed. No user currently logged in"

        if setup.current_user.username == command_items[1]:
            return "Failed. Cannot delete logged in account."

        current_user_permissions = setup.current_user.permissions
        if current_user_permissions[0] == '0' and current_user_permissions[1] == '0':
            return "Failed. Restricted action"

        file = FileIO()
        account = file.readData(command_items[1], "Account")

        if account is None:
            print("Failed. Username doesn't exist.")
            return "Failed. Username doesn't exist."
        else:
            exists = file.deleteData(command_items[1], 'Account')
            return "Account " + command_items[1] + " successfully removed."

    def validateInputParameters(self, command_items):
        if len(command_items) != 2:
            return False
        return True
