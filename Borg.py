class BorgImpl(object):
    shared = {}
    def __init__(self):
        self.__dict__ = Borg.shared