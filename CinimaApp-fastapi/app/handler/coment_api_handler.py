from typing import Dict, List
from fastapi import APIRouter, HTTPException
from app.scheme.model_coment import (
    ComentCreateRequest,
    ComentResponse,
    ComentUpdateRequest,
)
from app.repositories.coment_repositoried import ComentRepository
from app.service.factory import get_service
from app.service.coment_service import ComentService
from app.utils.comon import SessionDep

from uuid import UUID

coment_router = APIRouter(prefix="/coment", tags=["Coment"])


@coment_router.post("create_coment/{user_id}/{film_id}/")
async def create_coment(
    async_session: SessionDep, data: ComentCreateRequest, film_id: UUID, user_id: UUID
) -> ComentResponse:
    coment_sev = await get_service(ComentService, ComentRepository, async_session)
    coment = await coment_sev.create_model(data.dict(), film_id, user_id)
    if not coment:
        raise HTTPException(detail="Не удалось создать коментарий")
    return ComentResponse.from_orm(coment)


@coment_router.get("s/")
async def get_comets(
    async_session: SessionDep,
) -> List[ComentResponse]:
    coment_sev = await get_service(ComentService, ComentRepository, async_session)
    coments = await coment_sev.get_models()
    return [ComentResponse.from_orm(coments) for coments in coments]


@coment_router.get("/{comnet_id}")
async def get_coment_coment_id(
    comnet_id: UUID, async_session: SessionDep
) -> ComentResponse:
    coment_sev = await get_service(ComentService, ComentRepository, async_session)
    coment = await coment_sev.get_model(comnet_id)
    if not coment:
        raise HTTPException(detail="Не найдено такой кометария", status_code=404)
    return ComentResponse.from_orm(coment)


@coment_router.put("/update/{comnet_id}")
async def update_coment(
    data: ComentUpdateRequest, comnet_id: UUID, async_session: SessionDep
) -> ComentResponse:
    coment_sev = await get_service(ComentService, ComentRepository, async_session)
    coment = await coment_sev.update_model(comnet_id, data.dict())
    if not coment:
        raise HTTPException(detail="Не найдено такой кометария ", status_code=404)
    return ComentResponse.from_orm(coment)


@coment_router.put("/update/like/{comnet_id}")
async def update_coment(coment_id: UUID, async_session: SessionDep) -> ComentResponse:
    coment_sev = await get_service(ComentService, ComentRepository, async_session)
    coment = await coment_sev.update_like(coment_id)
    if not coment:
        raise HTTPException(detail="Не найдено такой кометария ", status_code=404)
    return ComentResponse.from_orm(coment)


@coment_router.put("/update/unlike/{comnet_id}")
async def update_coment(coment_id: UUID, async_session: SessionDep) -> ComentResponse:
    coment_sev = await get_service(ComentService, ComentRepository, async_session)
    coment = await coment_sev.update_unlike(coment_id)
    if not coment:
        raise HTTPException(detail="Не найдено такой кометария ", status_code=404)
    return ComentResponse.from_orm(coment)


@coment_router.delete("/delete/{comnet_id}")
async def delete_coment(comnet_id: UUID, async_session: SessionDep) -> Dict[str, str]:
    coment_sev = await get_service(ComentService, ComentRepository, async_session)
    coment = await coment_sev.delete_model(comnet_id)
    if not coment:
        raise HTTPException(detail="Не найдено такой кометария ", status_code=404)
    return {"message": "Delete coment and db"}
