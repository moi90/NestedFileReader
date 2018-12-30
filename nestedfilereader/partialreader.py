from nestedfilereader import BaseReader

class PartialReader(BaseReader):
    """
    A reader for partial paths
    """

    def __init__(self, parent, prefix):
        self.parent = parent
        self.prefix = prefix

    def open(self, name, mode):
        return self.parent.open(os.path.join(self.prefix, name), mode)