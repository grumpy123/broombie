from .errors import BroombieNameError, BroombieNameConflictError


class Truth:
    def __init__(self, base_truth=None):
        self.scope = {}
        self.base_truth = base_truth

    def ground_truth(self):
        if self.base_truth is None:
            return self
        return self.base_truth.ground_truth()

    def __contains__(self, key):
        if key in self.scope:
            return True
        if self.base_truth and key in self.base_truth:
            return True
        return False

    def __getitem__(self, key):
        if key in self.scope:
            return self.scope[key]
        if self.base_truth and key in self.base_truth:
            return self.base_truth[key]

        raise BroombieNameError(key)

    def __setitem__(self, key, value):
        if key in self:
            raise BroombieNameConflictError(key)
        self.scope[key] = value
