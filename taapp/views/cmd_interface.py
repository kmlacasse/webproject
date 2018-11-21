import abc


class CmdInterface(abc.ABC):

    @abc.abstractmethod
    def action(self, command_input):
        pass

    @abc.abstractmethod
    def validateInputParameters(self, command_input):
        pass
