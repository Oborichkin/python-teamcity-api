class Base:
    def __init__(self):
        self.id = None
        self.name = None
        self.href = None
        self.webUrl = None

    @classmethod
    def from_obj(cls, obj):
        c = cls()
        for key, value in obj.items():
            setattr(c, key, value)
        return c

    @classmethod
    def many_from_list(cls, lst):
        return [cls.from_obj(c) for c in lst]

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.id}): {self.name}>"
