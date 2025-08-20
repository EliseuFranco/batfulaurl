from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from passlib.context import CryptContext


pwd_hash = CryptContext(schemes='bcrypt', deprecated='auto')

class Users(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(nullable=False)
    email : str
    password_hash: str = Field(nullable=False, alias='password_hash')

    urls: List["URLS"] = Relationship(back_populates='owner')


    @property
    def hash_password(self):
        return self.password_hash

    @hash_password.setter
    def hash_password(self, password : str):
        self.password_hash = pwd_hash.hash(password)
    
    @staticmethod
    def check_password(password: str, pass_hash : str):
        return pwd_hash.verify(password, pass_hash)