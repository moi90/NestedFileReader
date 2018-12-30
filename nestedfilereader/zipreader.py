from zipfile import ZipFile
import io
import os
import datetime

from nestedfilereader import BaseReader
from nestedfilereader.splitpath import SplitError, split_container_member


class ZipReader(BaseReader):
    @classmethod
    def register(cls, ext=".zip"):
        """
        Register this reader.

        Parameters:
            ext: File extension (default: .zip)
        """
        super().register(ext)

    def __init__(self, filename, fp=None):
        super().__init__(filename, fp)

        if fp is None:
            # Ignore mode
            self.fp = ZipFile(filename)
        else:
            self.fp = ZipFile(fp)

    def isfile(self, path):
        try:
            info = self.fp.getinfo(path)
        except KeyError:
            return False

        return not info.is_dir()

    def isdir(self, path):
        try:
            info = self.fp.getinfo(path)
        except KeyError:
            return False

        return info.is_dir()

    def open(self, name, mode="rb"):
        if self.isdir(name):
            return PartialReader(self, name)

        try:
            container_path, container_ext, member_path = split_container_member(
                name, self.isfile)
        except SplitError as e:
            # No valid member was found
            raise ValueError("Not a valid member {}".format(name))

        # Read ZIP member into BytesIO
        with self.fp.open(container_path, "r") as f_parent:
            buffer = io.BytesIO(f_parent.read())

        try:
            reader_cls = BaseReader.get_reader(container_ext)

            print(
                f"{reader_cls.__name__}({container_path}, fp={buffer}).open({member_path}, mode={mode})...")

            reader = reader_cls(container_path, fp=buffer)

            if member_path:
                return reader.open(member_path, mode=mode)
            return reader
        except KeyError as e:
            if not member_path:
                return buffer
            raise ValueError("Not a known container and non-empty member path: {}, {}".format(
                container_path, member_path)) from e

    def close(self):
        pass

    def imembers(self):
        for zinfo in self.fp.infolist():
            if zinfo.is_dir():
                continue

            ext = os.path.splitext(zinfo.filename)[1]
            try:
                reader_cls = BaseReader.get_reader(ext)
            except KeyError:
                dt = datetime.datetime(*zinfo.date_time).timestamp()
                yield (zinfo.filename, dt, zinfo.file_size)
            else:
                entry_fn = os.path.join(self.filename, zinfo.filename)
                with self.fp.open(zinfo.filename, "r") as f_parent:
                    buffer = io.BytesIO(f_parent.read())
                reader = reader_cls(entry_fn, fp=buffer)
                for subentry in reader.imembers():
                    yield (os.path.join(entry_fn, subentry[0]),) + subentry[1:]
