from uuid import uuid4
from pydantic import Field
from decimal import Decimal
from pydantic import BaseModel
from pydantic.types import UUID4
from typing import List, Optional

from app.repository.lawyers import LawyersRepository

# class Ingredients(BaseModel):
#     name: str = Field(..., example='Rice')
#     uom: str = Field(..., example='Liter')
#     amount: Decimal = Field(..., example=2.5)

class LawyersModel(BaseModel):
    uid: Optional[str] = None
    title: str = Field(..., example='Lawyer Title')
    name: str = Field(..., example='John Doe')
    location: str = Field(..., example='North Pole')
    phone: str = Field(..., example='(999)999-9999')
    description: Optional[str] = Field(..., example='What makes this lawyer special')
    expertise: Optional[str] = Field(..., example='specialization')


class LawyersDomain():
    def __init__(self, repository: LawyersRepository) -> None:
        self.__repository = repository

    def get_all(self):
        return self.__repository.get_all()

    def get_lawyer(self, uid: str):
        return self.__repository.get_lawyer(uid)

    def create_lawyer(self, lawyer: LawyersModel):
        lawyer.uid = str(uuid4())
        return self.__repository.create_lawyer(lawyer.dict())

    def update_lawyer(self, lawyer: LawyersModel):
        return self.__repository.update_lawyer(lawyer.dict())

    def delete_lawyer(self, uid: str):
        return self.__repository.delete_lawyer(uid)