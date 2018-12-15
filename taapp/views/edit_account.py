from . import setup
from .cmd_interface import CmdInterface
from .file_io import FileIO
from ..models import Account


class EditAccount(CmdInterface):

    def action(self, command_input):
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters"

        if setup.current_user is None:
            return "Failed. No user currently logged in"

        if setup.current_user.username != command_items[1]:
            current_user_permissions = setup.current_user.permissions
            if current_user_permissions[0] != '1' and current_user_permissions[1] != '1':
                return "Failed. Restricted action"

        file = FileIO()
        user_check = file.readData(command_items[1], 'Account')
        if user_check is None:
            return "Failed. Username doesn't exist"
        field = command_items[2]
        user = Account.objects.get(username=command_items[1])
        if field == 'name':
            user_name = ""
            for word in command_items[3:]:
                user_name += word + " "
            user.name = user_name
        if field == 'address':
            address = ""
            for word in command_items[3:]:
                address += word + " "
            user.address = address
        if field == 'officehours':
            officehours = ""
            for word in command_items[3:]:
                officehours += word + " "
            user.officehours = officehours
        if field == 'password':
            user.password = command_items[3]
        if field == 'phone':
            user.phone = command_items[3]
        if field == 'email':
            user.email = command_items[3]
        user.save()

        return "Account " + command_items[1] + " successfully modified"

    def validateInputParameters(self, command_input):
        if len(command_input) < 4:
            return False

        return True


class ChangePassword(CmdInterface):

    def action(self, command_input):
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters"

        if setup.current_user is None:
            return "Failed. No user currently logged in"

        if setup.current_user.username != command_items[1]:
            current_user_permissions = setup.current_user.permissions
            if current_user_permissions[0] != '1' and current_user_permissions[1] != '1':
                return "Failed. Restricted action"

        file = FileIO()
        user_check = file.readData(command_items[1], 'Account')
        if user_check is None:
            return "Failed. Username doesn't exist"

        user = Account.objects.get(username=command_items[1])
        user.password = command_items[2]
        user.save()

        return command_items[1] + " password successfully changed"

    def validateInputParameters(self, command_items):
        if len(command_items) != 3:
            return False

        return True


class EditName(CmdInterface):

    def action(self, command_input):
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters"

        if setup.current_user is None:
            return "Failed. No user currently logged in"

        if setup.current_user.username != command_items[1]:
            current_user_permissions = setup.current_user.permissions
            if current_user_permissions[0] != '1' and current_user_permissions[1] != '1':
                return "Failed. Restricted action"

        file = FileIO()
        user_check = file.readData(command_items[1], 'Account')
        if user_check is None:
            return "Failed. Username doesn't exist"

        user = Account.objects.get(username=command_items[1])

        # Address can have spaces so group all parts together
        address = ""
        for word in command_items[2:]:
            address += word + " "

        user.address = address
        user.save()

        return "Address successfully changed"

    def validateInputParameters(self, command_items):
        if len(command_items) < 3:
            return False

        return True


class EditAddress(CmdInterface):

    def action(self, command_input):
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters"

        if setup.current_user is None:
            return "Failed. No user currently logged in"

        if setup.current_user.username != command_items[1]:
            current_user_permissions = setup.current_user.permissions
            if current_user_permissions[0] != '1' and current_user_permissions[1] != '1':
                return "Failed. Restricted action"

        file = FileIO()
        user_check = file.readData(command_items[1], 'Account')
        if user_check is None:
            return "Failed. Username doesn't exist"

        user = Account.objects.get(username=command_items[1])

        # Address can have spaces so group all parts together
        address = ""
        for word in command_items[2:]:
            address += word + " "

        user.address = address
        user.save()

        return "Address successfully changed"

    def validateInputParameters(self, command_items):
        if len(command_items) < 3:
            return False

        return True


class EditPhoneNumber(CmdInterface):

    def action(self, command_input):
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters"

        if setup.current_user is None:
            return "Failed. No user currently logged in"
        if setup.current_user.username != command_items[1]:
            current_user_permissions = setup.current_user.permissions
            if current_user_permissions[0] != '1' and current_user_permissions[1] != '1':
                return "Failed. Restricted action"

        file = FileIO()
        user_check = file.readData(command_items[1], 'Account')
        if user_check is None:
            return "Failed. Username doesn't exist"

        user = Account.objects.get(username=command_items[1])
        user.phone = command_items[2]
        user.save()

        return "Phone number successfully changed"

    def validateInputParameters(self, command_items):
        if len(command_items) != 3:
            return False

        return True


class EditEmail(CmdInterface):

    def action(self, command_input):
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)

        if not valid_params:
            return "Failed. Invalid parameters"

        if setup.current_user is None:
            return "Failed. No user currently logged in"

        if setup.current_user.username != command_items[1]:
            current_user_permissions = setup.current_user.permissions
            if current_user_permissions[0] != '1' and current_user_permissions[1] != '1':
                return "Failed. Restricted action"

        file = FileIO()
        user_check = file.readData(command_items[1], 'Account')
        if user_check is None:
            return "Failed. Username doesn't exist"

        user = Account.objects.get(username=command_items[1])
        user.email = command_items[2]
        user.save()

        return "Email successfully changed"

    def validateInputParameters(self, command_items):
        if len(command_items) != 3:
            return False

        return True
