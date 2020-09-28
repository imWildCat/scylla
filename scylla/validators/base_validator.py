

class BaseValidator(object):

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__

    def validate(self, proxy_str: str) -> bool:
        raise NotImplementedError

