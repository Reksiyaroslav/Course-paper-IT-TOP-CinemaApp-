from typing import Dict, List
from fastapi import APIRouter, HTTPException
from app.scheme.model_author import (
    AuthorResponse,
    AuthorUpdateRequest,
    AuthorCreateRequest,
)
from app.repositories.author_repositore import AuthorRepository
from app.service.factory import get_service
from app.service.author_service import AuthorService
from app.utils.comon import SessionDep

from uuid import UUID

author_router = APIRouter(prefix="/author", tags=["Author"])


@author_router.post("/")
async def create_author(
    data: AuthorCreateRequest, async_session: SessionDep
) -> AuthorResponse:
    author_sev = await get_service(AuthorService, AuthorRepository, async_session)
    author = await author_sev.create_model(data.dict())
    if not author:
        raise HTTPException(status_code=401, detail="not create author")
    return AuthorResponse.from_orm(author)


@author_router.get("s/")
async def get_authors(
    async_session: SessionDep,
) -> List[AuthorResponse]:
    author_sev = await get_service(AuthorService, AuthorRepository, async_session)
    authors = await author_sev.get_models()
    return [AuthorResponse.from_orm(actor) for actor in authors]


@author_router.get("/{actor_id}")
async def get_author_id(author_id: UUID, async_session: SessionDep) -> AuthorResponse:
    author_sev = await get_service(AuthorService, AuthorRepository, async_session)
    author = await author_sev.get_model(author_id)
    if not author:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return AuthorResponse.from_orm(author)


@author_router.get("/name_authors/{fistname_latname_pat}")
async def get_name_author(fistname_latname_pat: str, async_session: SessionDep):
    author_sev = await get_service(AuthorService, AuthorRepository, async_session)
    author = await author_sev.get_fistname_lastname_pat(fistname_latname_pat)
    if not author:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return AuthorResponse.from_orm(author)


@author_router.get("/name_authors/{fistname_latname_pat}")
async def get_name_authors(
    fistname_latname_pat: str, async_session: SessionDep
) -> AuthorResponse:
    author_sev = await get_service(AuthorService, AuthorRepository, async_session)
    author = await author_sev.get_serahc_name_list(fistname_latname_pat)
    if not author:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return AuthorResponse.from_orm(author)


@author_router.put("/update/{author_id}")
async def update_author(
    data: AuthorUpdateRequest, author_id: UUID, async_session: SessionDep
) -> AuthorResponse:
    author_sev = await get_service(AuthorService, AuthorRepository, async_session)
    author = await author_sev.update_model(author_id, data.dict())
    if not author:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return AuthorResponse.from_orm(author)


@author_router.delete("/delete/{author_id}")
async def delete_actor(author_id: UUID, async_session: SessionDep) -> Dict[str, str]:
    author_ser = await get_service(AuthorService, AuthorRepository, async_session)
    author = await author_ser.delete_model(author_id)
    if not author:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return {"message": "Delete actor and db"}
