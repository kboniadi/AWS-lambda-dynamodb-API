from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field
from pydantic.types import UUID4

from app.repository.lawyers_repository import LawyersRepository


class Expertise(str, Enum):
    h1b = "H1B"
    opt = "OPT"
    cpt = "CPT"
    f1_visa = "F1 Visa"
    j1_visa = "J1 Visa"

class LawyersModel(BaseModel):
    email: str = Field(..., example='example@cfgi.com')
    profile_url: str = Field(..., example='http://example.com')
    title: str = Field(..., example='Lawyer Title')
    name: str = Field(..., example='John Doe')
    languages: List[str] = Field(..., example=["English", "Spanish"])
    location: str = Field(..., example='California')
    phone: str = Field(..., example='(999)999-9999')
    description: Optional[str] = Field(..., example='What makes this lawyer special')
    expertise: Optional[List[Expertise]] = Field(..., example=["H1B", "OPT", "CPT", "F1 Visa", "J1 Visa"])


class LawyersDomain():
    def __init__(self, repository: LawyersRepository) -> None:
        self.__repository = repository

    def get_all(self):
        return self.__repository.get_all()

    def get_lawyer(self, email: str):
        return self.__repository.get_lawyer(email)

    def create_lawyer(self, lawyer: LawyersModel):
        return self.__repository.create_lawyer(lawyer.dict())

    def update_lawyer(self, lawyer: LawyersModel):
        return self.__repository.update_lawyer(lawyer.dict())

    def delete_lawyer(self, email: str):
        return self.__repository.delete_lawyer(email)