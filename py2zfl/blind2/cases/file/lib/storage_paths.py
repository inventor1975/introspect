import os

STORAGE_ROOT = "/srv/app/storage"


def member_dir(member_id):
    return os.path.join(STORAGE_ROOT, "members", str(member_id))


def member_file(member_id, name):
    folder = member_dir(member_id)
    return os.path.join(folder, name)


def read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()
