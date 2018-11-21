import abc


class IOInterface(abc.ABC):

    @abc.abstractmethod
    def readData(self, key, database):
        pass

    @abc.abstractmethod
    def writeData(self, key, filename, new_info):
        pass
