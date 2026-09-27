import os


class ExportLocator:
    def __init__(self, root):
        self.root = root

    def locate(self, name):
        return os.path.join(self.root, name)

    def locate_dated(self, day, name):
        return os.path.join(self.root, day.strftime("%Y/%m"), name)
