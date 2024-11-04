from datetime import datetime
import base64
from uuid import uuid4
from fastapi import HTTPException

from passlib.context import CryptContext
from src.schema.schema import RegisterSchema, LoginSchema, ForgotPasswordSchema
from src.model import Person, Users, Role
from src.repository.role import RoleRepository
from src.repository.users import UsersRepository
from src.repository.person import PersonRepository
from src.repository.user_role import UsersReleRepository
from src.repository.auth_repo import JWTRepo
import os
from pathlib import Path

#Encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    
    @staticmethod
    async def register_service(register: RegisterSchema):

        # Create uuid
        _person_id = str(uuid4())
        _user_id = str(uuid4())
        
        # convert birth date type from frontend str to datetime
        birth_date = datetime.strptime(register.birth, "%d-%m-%Y").date()
        
        # open image profile default to base64 string
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        profile_path = os.path.join(BASE_DIR, "media", "profile.png")
        
        #Then use it in your code
        with open(profile_path, "rb") as f:
            image_str = base64.b64encode(f.read())
        image_str = "data:image/png;base64," + image_str.decode('utf-8')
        
        # mapping request data to class entity table 
        _person = Person (id=_person_id, name=register.name, birth = birth_date, sex= register.sex,
                          profile = image_str, phone_number = register.phone_number)
        
        _users = Users(id=_user_id,name = register.name, username= register.username, email= register.email,
                       password = pwd_context.hash(register.password),
                       person_id=_person_id,
                       )
        
        # Everyone who registers through our registration page makes the default user
        _role = await RoleRepository.find_by_role_name("user")
        _users_role = UsersReleRepository(users_id=_user_id, role_id=_role.id)
        
        # Checking the same username
        _username = await UsersRepository.find_by_username(register.username)
        if _username:
            raise HTTPException(status_code=400, detail="Username already exists!")
        
        # Checking the same email
        _email = await UsersRepository.find_by_email(register.email)
        if _email:
            raise HTTPException(status_code=400, detail="Email already exists!")
        
        else:
            # Insert to tables
            await PersonRepository.create(**_person.dict())
            await UsersRepository.create(**_users.dict())
            await UsersReleRepository.create(**_users_role.dict())
        
    @staticmethod
    async def login_service(login: LoginSchema):
        _username = await UsersRepository.find_by_username(login.username)
            
        if _username is not None:
            if not pwd_context.verify(login.password, _username.password):
                raise HTTPException(status_code=400, detail="Invalid Password!")
            return JWTRepo(data={"username": _username.username}).generate_token()
        raise HTTPException(status_code=400, detail="Username not found!")
        
    @staticmethod
    async def forgot_password_service(forgot_password: ForgotPasswordSchema):
        _email = await UsersRepository.find_by_email(forgot_password.email)
        
        if _email is None:
            raise HTTPException(status_code=404, detail="Email not found!")
        await UsersRepository.update_password(forgot_password.email, pwd_context.hash(forgot_password.new_password))
        
#Generate roles manually
async def generate_role():
    _role = await RoleRepository.find_by_list_role_name(["admin", "user"])
    if not _role:
        await RoleRepository.create_list([Role(id=str(uuid4()), role_name="admin"), Role(id=str(uuid4()), role_name="user")])