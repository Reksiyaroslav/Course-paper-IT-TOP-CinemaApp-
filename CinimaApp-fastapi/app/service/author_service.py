from app.service.base_service import Base_Service
from uuid import UUID
from fastapi.exceptions import HTTPException
from app.utils.comon import is_fistname_lastname, validate_is_data_range
from app.list.list_searhc import list_serach_date
from ..db.model.model_db import Author
from app.repositories.author_repositore import AuthorRepository


class AuthorService(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.author_repo = AuthorRepository(self.session)

    async def create_author(self, data, name_title_value=None):
        if not validate_is_data_range(data[list_serach_date[1]], "author"):
            raise HTTPException(
                detail="Что не так с дадой рождения возможно не находится дипозоне 1945-2025",
                status_code=400,
            )
        elif not await is_fistname_lastname(Author, self.author_repo.session, data):
            raise HTTPException(detail="Такой  автор существует", status_code=400)
        return await self.author_repo.create_author(data)

    async def update_author(self, author_id, data):
        if not validate_is_data_range(data[list_serach_date[1]], "Author".lower()):
            raise HTTPException(
                detail="Что не так сдадой рождения возможно не находится дипозоне 1945-2025",
                status_code=400,
            )
        elif not await is_fistname_lastname(Author, self.author_repo.session, data):
            raise HTTPException(detail="Тайокй автор существует", status_code=400)

        return await self.author_repo.update_author(data, author_id)

    async def delete_author(self, author_id):
        return await self.author_repo.delete_author(author_id)

    async def get_authors(self):
        return await self.author_repo.get_authors()

    async def get_author_by_id(self, author_id):
        return await self.author_repo.get_author_by_id(author_id)

    async def get_fistname_lastname_pat_list(self, name: str):
        return await self.author_repo.get_author_fistname_latname_pat_list(name)
