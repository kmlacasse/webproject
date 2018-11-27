class Command:

    def __init__(self):
        self.command_dict = {}

    def containsCommand(self, command_input):
        if command_input in self.command_dict:
            return 1
        return 0

    def commandDictLength(self):
        return len(self.command_dict)

    def callCommand(self, command_input):
        cmd = command_input.split()
        found_command = False
        response = ''
        if self.containsCommand(cmd[0]):
            found_command = True
            response = self.command_dict[cmd[0]].action(command_input)
        if not found_command:
            return "Failed. No such command"
        return response

    def addCommand(self, command, command_object):
        self.command_dict[command] = command_object
