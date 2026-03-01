from typing import Dict, List
from fastapi import APIRouter, HTTPException
from app.scheme.model_author import (
    AuthorResponse,
    AuthorUpdateRequest,
    AuthorCreateRequest,
)
from app.utils.comon import Depends
from app.utils.depencines import AuthorService, get_author_service
from uuid import UUID

author_router = APIRouter(prefix="/author", tags=["Author"])


@author_router.post("/")
async def create_author(
    data: AuthorCreateRequest,
    author_service: AuthorService = Depends(get_author_service),
) -> AuthorResponse:
    author = await author_service.create_author(data.dict())
    if not author:
        raise HTTPException(status_code=401, detail="not create author")
    return AuthorResponse.from_orm(author)


@author_router.get("s/")
async def get_authors(
    author_service: AuthorService = Depends(get_author_service),
) -> List[AuthorResponse]:
    authors = await author_service.get_authors()
    return [AuthorResponse.from_orm(author) for author in authors]


@author_router.get("/profile/{actor_id}")
async def get_author_id(
    author_id: UUID, author_service: AuthorService = Depends(get_author_service)
) -> AuthorResponse:
    author = await author_service.get_author_by_id(author_id)
    if not author:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return AuthorResponse.from_orm(author)


@author_router.get("/name_authors/{fistname_latname_pat}")
async def get_name_authors(
    fistname_latname_pat: str,
    author_service: AuthorService = Depends(get_author_service),
) -> List[AuthorResponse]:
    authors = await author_service.get_fistname_lastname_pat_list(fistname_latname_pat)
    if not authors:
        raise HTTPException(detail="Не найдено такой актёры", status_code=404)
    return [AuthorResponse.from_orm(author) for author in authors]


@author_router.put("/update/{author_id}")
async def update_author(
    data: AuthorUpdateRequest,
    author_id: UUID,
    author_service: AuthorService = Depends(get_author_service),
) -> AuthorResponse:
    author = await author_service.update_author(author_id, data.dict())
    if not author:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return AuthorResponse.from_orm(author)


@author_router.delete("/delete/{author_id}")
async def delete_actor(
    author_id: UUID, author_service: AuthorService = Depends(get_author_service)
) -> Dict[str, str]:
    author = await author_service.delete_author(author_id)
    if not author:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return {"message": "Delete actor and db"}
