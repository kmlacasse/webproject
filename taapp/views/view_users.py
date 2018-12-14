from . import setup
from .cmd_interface import CmdInterface
from ..models import Account


class ViewUsers(CmdInterface):

    def action(self, command_input):

        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters"

        if setup.current_user is None:
            return "Failed. No user currently logged in"

        # Get a list of all Accounts
        accountList = Account.objects.all()
        ret = []

        # The accountList has to be at least one because there is a user logged in
        for i in range(accountList.count()):
            ret.append([accountList[i].username, accountList[i].name])

        return ret

    def validateInputParameters(self, command_items):
        NUM_PARAMS = 1

        if len(command_items) == NUM_PARAMS:
            return True
        return False
