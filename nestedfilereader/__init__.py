from nestedfilereader.fsreader import FSReader
from nestedfilereader.basereader import BaseReader
from nestedfilereader.splitpath import split_container_member, SplitError

import os
import io

def open(name, mode="r"):
    # Name may be a pathlib.Path
    if not isinstance(name, str):
        name = str(name)

    # If name is a directory, return a file-system reader
    if os.path.isdir(name):
        return FSReader(name)

    try:
        container_path, container_ext, member_path = split_container_member(
            name, os.path.isfile)
    except SplitError as e:
        # No valid container was found
        raise ValueError("Not a valid name: {}".format(name)) from e

    try:
        reader = BaseReader.get_reader(container_ext)
    except KeyError as e:
        if not member_path:
            # If member_path is is empty, return a file handle for container_path
            return io.open(name, mode)
        else:
            # There is no reader for the container
            raise ValueError("Not a known container extension and non-empty member path: {}, {}".format(
                container_path, member_path)) from e

    # Use the reader to open the member
    if member_path:
        # TODO: Close the reader when the member is closed
        print(f"{reader.__name__}({container_path}).open({member_path}, mode={mode})...")
        return reader(container_path).open(member_path, mode=mode)
    
    return reader(container_path)
