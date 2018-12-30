import datetime
import io
import operator
import os
import re

from zipfile import ZipFile

# def make_entry(entry):
#     if isinstance(entry, Entry):
#         return entry
#     mtime = os.path.getmtime(entry)
#     return Entry(entry, mtime)


# handlers = {
#     ".zip": (lambda x: None)
# }

# class DirectoryHandler:
#     def __init__(self, file):
#         self.file = file

#     def open(self, file, mode="r"):
#         raise NotImplementedError()

#     def namelist(self):
#         return os.listdir(self.file)


# class NestedIO:
#     """
#     File-like capable of opening nested archives.

#     Parameters:
#         file: Can be a string, path-like or file-like
#         root_path: Path of this container
#     """

#     _handlers = {}

#     @staticmethod
#     def register_handler(extension, handler):
#         NestedIO._handlers[extension] = handler

#     def __init__(self, file, mode="r", root_path=None, parent=None):
#         print("NestedIO({!r}, {!r}, {!r}, {!r})".format(file, mode, root_path, parent))
#         self.fp = None

#         if isinstance(file, os.PathLike):
#             file = os.fspath(file)
#         if isinstance(file, str):
#             if root_path is not None:
#                 if not os.path.commonpath((file, root_path)) == root_path:
#                     raise ValueError("{} is not below {}.".format(file, root_path))
#                 rel_path = os.path.relpath(file, root_path)
#             else:
#                 rel_path = file

#             # First, see if this "container" is actually a directory
#             if os.path.isdir(file):
#                 print("{} is a dir.".format(file))
#                 self.fp = DirectoryHandler(file)
#             elif os.path.isfile(file):
#                 print("{} is a file.".format(file))
#                 ext = os.path.splitext(file)[1]
#                 try:
#                     handler = NestedIO._handlers[ext]
#                 except KeyError:
#                     handler = io.open
#                 print("Handler is {!r}.".format(handler))
#                 self.fp = handler(file, mode=mode)
#             else:
#                 # Find occurences of container filenames in the path
#                 # ".[ext]/" in file or file.endswith(".[ext]")
#                 match = container_ext_re.search(rel_path)
#                 if match is not None:
#                     # TODO: Eliminate the possibility that this is just a folder with an extension
#                     # (This can be handled implicitely)

#                     ext = match[1]
#                     # Open the path up to the match
#                     parent_path, child_path = rel_path[:match.end(1)], rel_path[match.end(1)+1:]
#                     print(parent_path, child_path)
#                     parent_root_path = os.path.join(root_path, parent_path) if root_path is not None else parent_path

#                     print("Recursion into {}.".format(parent_path))
#                     parent = NestedIO(parent_path, mode, root_path=parent_root_path, parent=self)
#                     self.fp = parent.open(child_path)

#             # Easy case (fp is still None):
#             if self.fp is None:
#                 raise ValueError("{!r} could not be opened.".format(file))
#         else:
#             self.fp = file
#             self.name = root_path or getattr(file, 'name', None)

#     def __repr__(self):
#         return "NestedIO(fp={})".format(self.fp)

#     def open(self, member):
#         """
#         Open a member.
#         """
#         print("{!r}.open({})...".format(self, member))
#         return self.fp.open(member)

#     def read(self):
#         pass

#     def write(self):
#         pass

#     def list(self):
#         """
#         List members.
#         """
#         pass


# # ZipFile()


# class ZipHandler:
#     def __init__(self, file, mode="r"):
#         self.file = ZipFile(file, mode)

#     def namelist(self):
#         return self.file.namelist()

#     def open(self, file, mode="r"):
#         print("ZipHandler.open({})".format(file))
#         return self.file.open(file, mode)


# NestedIO.register_handler(".zip", ZipHandler)

# # ufo = NestedIO()

# # with NestedIO("foo.zip") as root:
# #     with root.open("bar.txt") as f:
# #         print(f.read())

# # with NestedIO("foo.zip/bar.zip/baz.txt") as f:
# #     print(f.read())

# # with NestedIO("foo.zip/bar.zip") as f:
# #     f.read()  # Read whole file
# #     f.list()  # List file members


# # def recurse(entries):
# #     working_table = list(entries)

# #     while working_table:
# #         entry = working_table.pop()
# #         ext = os.path.splitext(entry)[0]
# #         if ext in handlers:
# #             working_table.extend(handlers[ext](entry))
# #         else:
# #             yield entry


# NestedIO("/home/moi/Work/Work.zip/test.zip/test.c")



















# with ZipFile("/home/moi/Work/zip-test/Work.zip") as z1:
#     with z1.open("test.zip", "r") as z2:
#         buffer = io.BytesIO(z2.read())
#         with ZipFile(buffer).open("test/test.c") as f:
#             print(f.read())
# # is equivalent to:
# with open("/home/moi/Work/zip-test/Work.zip/test.zip/test/test.c", "r") as f:
#     print(f.read())


# # Fails because test2.zip is in fact only a directory inside Work.zip
# with open("/home/moi/Work/zip-test/Work.zip/test2.zip/bar.txt", "r") as f:
#     print(f.read())

# with open("/home/moi/Work/zip-test/test2.zip", "r") as f1:
#     print(f1.members())
#     with f1.open("bar.txt", "r") as f2:
#         print(f2.read())

with open("/home/moi/Work/zip-test") as root:
    for member in root.imembers():
        print(member)
