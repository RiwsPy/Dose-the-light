class f_base(int):
    pass


class f_entity(f_base):
    def __new__(cls, **kwargs):
        return super().__new__(cls, kwargs['id'])

    def __init__(self, **kwargs) -> None:
        self.tags = {}
        self.owner = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    """
    @property
    def properties(self):
        return self.tags['properties']

    @properties.setter
    def properties(self, value) -> None:
        self.tags['properties'] = value
    """

    @property
    def name(self) -> str:
        return self.tags.get('name', '')

    @name.setter
    def name(self, value: str) -> None:
        self.tags['name'] = value

    @property
    def __dict__(self):
        cpy = super().__dict__.copy()
        try:
            del cpy['owner']
        except KeyError:
            pass
        return cpy
