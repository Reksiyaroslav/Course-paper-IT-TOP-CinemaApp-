from litestar import get, Controller, post, put, delete

from app.repositories.coment_repositoried import ComentRepository
from app.model.model_coment import (
    ComentCreateRequest,
    ComentResponse,
    ComentUpdateRequest,
)
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from litestar.exceptions import HTTPException
from typing import Dict

from litestar.di import Provide
from app.service.coment_service import ComentService
from app.service.factory import get_service


class ComentControlle(Controller):
    path = "/coment"
    tags = ["❌Coment"]

    @post()
    async def create_coment(
        self, data: ComentCreateRequest, async_session: AsyncSession
    ) -> ComentResponse:
        coment_service = get_service(ComentService, ComentRepository, async_session)
        coment = await coment_service.create_model(data.dict())
        if not coment:
            raise HTTPException("Not coment", status_code=404)
        return ComentResponse.from_orm(coment)

    @get()
    async def get_list_coment(
        self, async_session: AsyncSession
    ) -> list[ComentResponse]:
        coment_service = get_service(ComentService, ComentRepository, async_session)
        coments = await coment_service.get_models()
        return [ComentResponse.from_orm(coment) for coment in coments]

    @get("film/{film_id:uuid}")
    async def get_comets_film(
        self, film_id: UUID, async_session: AsyncSession
    ) -> list[ComentResponse]:
        coment_service = get_service(ComentService, ComentRepository, async_session)
        coments = await coment_service.list_film_coments(film_id)
        return [ComentResponse.from_orm(coment) for coment in coments]

    @get("user/{user_id:uuid}")
    async def get_comets_user(
        self, user_id: UUID, async_session: AsyncSession
    ) -> list[ComentResponse]:
        coment_service = get_service(ComentService, ComentRepository, async_session)
        coments = await coment_service.list_user_coments(user_id)
        return [ComentResponse.from_orm(coment) for coment in coments]

    @get("{coment_id:uuid}")
    async def get_coment_id(
        self, coment_id: UUID, async_session: AsyncSession
    ) -> ComentResponse:
        coment_service = get_service(ComentService, ComentRepository, async_session)
        coment = await coment_service.get_model(coment_id)
        return ComentResponse.from_orm(coment)

    @put("{coment_id:uuid}")
    async def update_coment(
        self, coment_id: UUID, data: ComentUpdateRequest, async_session: AsyncSession
    ) -> ComentResponse:
        coment_service = get_service(ComentService, ComentRepository, async_session)
        coment = await coment_service.update_model(coment_id, data.dict())
        if not coment:
            raise HTTPException("Not coment", status_code=404)
        return ComentResponse.from_orm(coment)

    @delete("{coment_id:uuid}", status_code=200)
    async def delete_coment(self, coment_id: UUID, async_session: AsyncSession) -> dict:
        coment_service = get_service(ComentService, ComentRepository, async_session)
        coment = await coment_service.delete_model(coment_id)
        if not coment:
            raise HTTPException("Not coment", status_code=404)
        return {"detali": "Coment delete db"}
