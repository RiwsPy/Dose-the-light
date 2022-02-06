from . import f_entity


class f_relation(f_entity):
    def __init__(self, *args, **kwargs):
        self.type = 'relation'
        super().__init__(*args, **kwargs)
        self.nodes = []
        self.ways = []
