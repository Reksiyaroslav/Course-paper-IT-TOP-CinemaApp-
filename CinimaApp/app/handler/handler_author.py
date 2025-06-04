from litestar import get ,Controller,post,put,delete
from litestar.params import Dependency
from app.repositories.author_repositore import AuthorRepository
from app.model.model_author import AuthorCreateRequest,AuthorResponse,AuthorlListResponse,AuthorUpdateRequest
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from litestar.exceptions import HTTPException
from typing import Dict
class AuthorControlle(Controller):
    path = "/author"
    tags =["Author"]
    security =[]
    @post()
    async def create_author(self,data:AuthorCreateRequest,async_session:AsyncSession =Dependency())->AuthorResponse:
        author_repo = AuthorRepository(async_session)
        author =  await author_repo.create(data.dict())
        return AuthorResponse.from_orm(author)
    @get()
    async def get_list_author(self,async_session:AsyncSession =Dependency())->list[AuthorResponse]:
        author_repo = AuthorRepository(async_session)
        authors =  await author_repo.get_list_model()
        return [AuthorResponse.from_orm(author)  for author in authors ]
    @get("id/{author_id:uuid}")
    async def get_author_id(self,author_id:UUID,async_session:AsyncSession =Dependency())->AuthorResponse:
        author_repo = AuthorRepository(async_session)
        author =  await author_repo.get_author_id(author_id)
        if not author:
            raise HTTPException("Not Author" ,status_code=404)
        return AuthorResponse.from_orm(author)
    @get("name/{author_fistname_lastname_pat:str}")
    async def get_author_fistname_lastname_pat(self,author_fistname_lastname_pat:str,async_session:AsyncSession =Dependency())->AuthorResponse:
        author_repo = AuthorRepository(async_session)
        author =  await author_repo.get_author_fistname_latname_pat(author_fistname_lastname_pat)
        if not author:
            raise HTTPException("Not Author" ,status_code=404)
        return AuthorResponse.from_orm(author)
    @put("id/{author_id:uuid}" ,summary="Update film")
    async def update_user(self,author_id:UUID, data:AuthorUpdateRequest ,async_session:AsyncSession=Dependency())->AuthorResponse:
        author_repo   = AuthorRepository(async_session)
        author = await author_repo.update_model(author_id,data.dict(exclude_unset=True))
        if not author:
            raise HTTPException(status_code=404,detail="Not author")
        return AuthorResponse.from_orm(author)

