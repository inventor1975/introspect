"""Small filesystem helpers shared by the document and report views."""
import os


def join_under(base, name):
    """Build the on-disk location of ``name`` inside ``base``."""
    name = name.strip()
    return os.path.join(base, name)


def resolve_inside(base, name):
    """Return the absolute location of ``name`` under ``base``.

    Raises ValueError when the result would leave ``base``.
    """
    root = os.path.realpath(base)
    candidate = os.path.realpath(os.path.join(root, name))
    if os.path.commonpath([root, candidate]) != root:
        raise ValueError("path escapes storage root")
    return candidate


class DiskStore:
    """Flat blob store backed by a directory."""

    def __init__(self, root):
        self.root = root

    def location(self, key):
        return os.path.join(self.root, key)

    def read_bytes(self, key):
        with open(self.location(key), "rb") as fh:
            return fh.read()

    def write_bytes(self, key, data):
        with open(self.location(key), "wb") as fh:
            fh.write(data)
