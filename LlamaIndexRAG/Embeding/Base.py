class BaseEmbed:
    def __init__(self,name) -> None:
        self.name = name
    def get_embeding(self):
        raise NotImplementedError