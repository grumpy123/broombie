class BroombieError(RuntimeError):
    pass


class BroombieParseError(BroombieError):
    def __init__(self, token):
        super().__init__("Don't know how to parse '{t}'.".format(t=token))
        self.token = token


class BroombieNameError(BroombieError):
    def __init__(self, key):
        super().__init__("Unknown value: '{key}'.".format(key=key))
        self.key = key


class BroombieNameConflictError(BroombieError):
    def __init__(self, key):
        super().__init__("Value '{key}' already exists.".format(key=key))
        self.key = key


class BroombieInternalError(BroombieError):
    pass
