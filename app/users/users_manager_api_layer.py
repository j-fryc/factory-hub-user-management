from app.utils.api_handler import BaseApiLayer


class UserManagerApiLayer(BaseApiLayer):
    def __init__(self, auth_url: str):
        super().__init__(auth_url=auth_url)
