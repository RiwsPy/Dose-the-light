class f_entity(int):
    def __new__(cls, **kwargs):
        return super().__new__(cls, kwargs['id'])

    def __init__(self, **kwargs) -> None:
        self.tags = {}
        self.owner = None
        self.properties = {}
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def properties(self):
        return self.tags['properties']

    @properties.setter
    def properties(self, value) -> None:
        self.tags['properties'] = value

    @property
    def name(self) -> str:
        return self.tags.get('name', '')

    @name.setter
    def name(self, value: str) -> None:
        self.tags['name'] = value
