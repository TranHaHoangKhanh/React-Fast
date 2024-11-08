from src.model.person import Person
from src.repository.base_repo import BaseRepo

class PersonRepository(BaseRepo):
    model = Person