from fastapi import HTTPException, status
from app.utils.comon import is_fistname_lastname, validate_is_data_range
from ..db.model.model_db import Author
from app.repositories.author_repositore import AuthorRepository
from app.enums.serach_fileld import SerachFiled
from app.enums.type_model import TypeModel
from app.utils.noramliz_text import normalize_data, text_strip_lower
from app.service.base_service import Base_Service
from app.scheme.author.model_author import AuthorResponse, AuthorlListResponse


class AuthorService(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.author_repo = AuthorRepository(self.session)

    async def create_author(self, data, name_title_value=None):
        filed_date = SerachFiled.Date.value[1]
        clean_data: dict = normalize_data(data=data, model_type=TypeModel.Author.value)
        if not validate_is_data_range(data[filed_date], TypeModel.Author.value):
            raise HTTPException(
                detail="Что не так с дадой рождения возможно не находится дипозоне 1945-2025",
                status_code=400,
            )
        elif not await is_fistname_lastname(
            Author, self.author_repo.session, clean_data
        ):
            raise HTTPException(detail="Такой  автор существует", status_code=400)
        new_author = await self.author_repo.create_author(clean_data)
        if not new_author:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при создании автора",
            )
        return AuthorResponse.from_orm(new_author)

    async def update_author(self, author_id, data):
        filed_date = SerachFiled.Date.value[1]
        clean_data: dict = normalize_data(data=data, model_type=TypeModel.Author.value)
        if not validate_is_data_range(data[filed_date], TypeModel.Author.value):
            raise HTTPException(
                detail="Что не так сдадой рождения возможно не находится дипозоне 1945-2025",
                status_code=400,
            )
        elif not await is_fistname_lastname(
            Author, self.author_repo.session, clean_data
        ):
            raise HTTPException(detail="Тайокй автор существует", status_code=400)
        update_author = await self.author_repo.update_author(clean_data, author_id)
        if not update_author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Автор не найден"
            )
        return AuthorResponse.from_orm(update_author)

    async def delete_author(self, author_id):
        success = await self.author_repo.delete_author(author_id)
        print(success)
        if not success:
            raise HTTPException(status_code=404, detail="Автор не найден")
        return {"message": "Автор успешно удалён"}

    async def get_authors(self):
        authors = await self.author_repo.get_authors()
        return AuthorlListResponse(author=authors)

    async def get_author_by_id(self, author_id):
        author = await self.author_repo.get_author_by_id(author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Автор не найден"
            )
        return AuthorResponse.from_orm(author)

    async def get_fistname_lastname_pat_list(self, name: str):
        norm_text = text_strip_lower(name)
        authors = await self.author_repo.get_author_fistname_latname_pat_list(norm_text)

        return AuthorlListResponse(author=authors)
