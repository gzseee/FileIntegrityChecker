class Plugin:
    extensions = []

    def __init__(self, conf):
        self.log = conf['log']

    def usable(self, file):
        file = file.lower()

        for ext in self.extensions:
            if file.endswith('.' + ext.lower()):
                return True

        return False
