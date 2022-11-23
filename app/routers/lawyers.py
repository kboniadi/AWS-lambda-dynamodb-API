from fastapi import APIRouter
from fastapi import HTTPException

from app.domain.lawyers import LawyersDomain, LawyersModel


class LawyersRouter:
    def __init__(self, lawyers_domain: LawyersDomain) -> None:
        self.__lawyers_domain = lawyers_domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/lawyers', tags=['lawyers'])
        
        @api_router.get('/')
        def index_route():
            return 'Hello! Welcome to lawyers index route'

        @api_router.post('/create')
        def create_lawyer(lawyers_model: LawyersModel):
            return self.__lawyers_domain.create_lawyer(lawyers_model)

        @api_router.get('/get/{lawyer_email}')
        def get_lawyer(lawyer_email: str):
            try:
                return self.__lawyers_domain.get_lawyer(lawyer_email)
            except KeyError:
                raise HTTPException(status_code=400, detail='No lawyer found')

        @api_router.put('/update')
        def update_lawyer(lawyers_model: LawyersModel):
            return self.__lawyers_domain.update_lawyer(lawyers_model)

        @api_router.delete('/delete/{lawyer_email}')
        def delete_lawyer(lawyer_email: str):
            return self.__lawyers_domain.delete_lawyer(lawyer_email)

        @api_router.get('/all')
        def get_all():
            return self.__lawyers_domain.get_all()

        return api_router