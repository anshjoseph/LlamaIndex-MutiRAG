from .provider_base import BaseProvider


class LanceDB(BaseProvider):
    def __init__(self, provider: str) -> None:
        super().__init__(provider)