from nestedfilereader.basereader import BaseReader

class FSReader(BaseReader):
    def __init__(self, filename, fp=None, mode="rb"):
        super().__init__(filename, fp)
        if fp is not None:
            self.fp = fp
        else:
            try:
                self.fp = io.open(filename, mode)
            except OSError:
                self.fp = None

    def close(self):
        if self.fp is not None:
            self.fp.close()

    def open(self, name, mode):
        # TODO: Use appropriate reader
        return FSReader(os.path.join(self.filename, name), mode=mode)

    def read(self, *args, **kwargs):
        if self.fp is not None:
            return self.fp.read(*args, **kwargs)
        return None

    def imembers(self):
        """
        Iterable of all files below this directory
        """
        if not os.path.isdir(self.filename):
            return

        queue = [self.filename]

        while queue:
            base_path = queue.pop()
            with os.scandir(base_path) as it:
                for entry in it:
                    if entry.is_file():
                        entry_fn = os.path.join(base_path, entry.name)
                        ext = os.path.splitext(entry.name)[1]
                        try:
                            reader = _container_readers[ext](entry_fn)
                        except KeyError:
                            stat = entry.stat()
                            yield (entry_fn, stat.st_mtime, stat.st_size)
                        else:
                            for subentry in reader.imembers():
                                yield (os.path.join(entry_fn, subentry[0]),) + subentry[1:]
                    elif entry.is_dir():
                        queue.append(os.path.join(base_path, entry.name))