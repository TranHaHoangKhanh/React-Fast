from src.model.user_role import UsersRole
from src.repository.base_repo import BaseRepo

class UsersReleRepository(BaseRepo):
    model = UsersRole
    
    def __init__(self, users_id: int = None, role_id: int = None):
        super().__init__()
        self.users_id = users_id
        self.role_id = role_id