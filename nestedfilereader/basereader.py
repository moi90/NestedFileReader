from abc import ABC, abstractmethod

class BaseReader(ABC):
    """
    Abstract base class for all readers.
    """

    __readers = {}

    @classmethod
    def register(cls, ext):
        BaseReader.__readers[ext] = cls

    @staticmethod
    def get_reader(ext):
        return BaseReader.__readers[ext]

    def __init__(self, filename, fp=None):
        self.filename = filename
        self.fp = fp
        pass

    @abstractmethod
    def open(self, name, mode):
        """
        Open a member.
        """
        pass

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return None

    @abstractmethod
    def imembers(self):
        """
        Iterable of all members of this container.
        """
        while False:
            yield None

    def members(self):
        return list(self.imembers())