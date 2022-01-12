from . import f_entity


class f_relation(f_entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nodes = []
        self.ways = []

    @property
    def __dict__(self):
        cpy = super().__dict__.copy()
        try:
            del cpy['owner']
        except KeyError:
            pass
        return cpy
