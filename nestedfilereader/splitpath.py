import re
import operator


class SplitError(ValueError):
    pass


__container_ext_re = re.compile(r"(\.[a-zA-Z0-9]+)(\/|$)")


def split_container_member(path, is_member):
    """
    Split a path into a container path and a member subpath.

    Parameters:
        path: The path that should be split.
        is_member: Callback to check if a path
            is a member of the parent container.

    Returns:
        A tuple (container_path, container_ext, member_path)

    Example:
        /hello/world.zip/foo/bar.txt -> (hello/world.zip, foo/bar.txt), given that 
        is_member(hello/world.zip) is true.
    """

    # Generate a list of hypotheses
    # (container_path, member_path)
    hypotheses = [(path[:match.end(1)], match[1], path[match.end(0):])
                  for match in __container_ext_re.finditer(path)]

    if not hypotheses:
        raise SplitError("No valid container member found: {}".format(path))

    # For each hypothesis: Check if the container path is a member of the parent container
    hvalid = map(lambda x: is_member(x[0]), hypotheses)

    split, valid = max(zip(hypotheses, hvalid), key=operator.itemgetter(1))

    if not valid:
        raise SplitError("No valid container member found: {}".format(path))

    return split
