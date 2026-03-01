from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends
from app.scheme.model_coment import (
    ComentCreateRequest,
    ComentResponse,
    ComentUpdateRequest,
)
from app.utils.depencines import ComentService, get_comment_service

from uuid import UUID

coment_router = APIRouter(prefix="/coment", tags=["Coment"])


@coment_router.post("create_coment/{user_id}/{film_id}/")
async def create_coment(
    data: ComentCreateRequest,
    film_id: UUID,
    user_id: UUID,
    coment_sev: ComentService = Depends(get_comment_service),
) -> ComentResponse:
    coment = await coment_sev.create_model(data.dict(), film_id, user_id)
    if not coment:
        raise HTTPException(detail="Не удалось создать коментарий", status_code=400)
    return ComentResponse.from_orm(coment)


@coment_router.get("s/")
async def get_comets(
    coment_sev: ComentService = Depends(get_comment_service),
) -> List[ComentResponse]:
    coments = await coment_sev.get_coments()
    return [ComentResponse.from_orm(coments) for coments in coments]


@coment_router.get("/{coment_id}")
async def get_coment_coment_id(
    comnet_id: UUID, coment_sev: ComentService = Depends(get_comment_service)
) -> ComentResponse:
    coment = await coment_sev.get_by_id_coment(comnet_id)
    if not coment:
        raise HTTPException(detail="Не найдено такой кометария", status_code=404)
    return ComentResponse.from_orm(coment)


@coment_router.put("/update/{coment_id}")
async def update_coment(
    data: ComentUpdateRequest,
    comnet_id: UUID,
    coment_sev: ComentService = Depends(get_comment_service),
) -> ComentResponse:
    coment = await coment_sev.update_coment(comnet_id, data.dict())
    if not coment:
        raise HTTPException(detail="Не найдено такой кометария ", status_code=404)
    return ComentResponse.from_orm(coment)


@coment_router.put("/update/like/{coment_id}")
async def update_coment_type_rec(
    coment_id: UUID,
    type_rec: str,
    user_id: UUID,
    coment_sev: ComentService = Depends(get_comment_service),
) -> ComentResponse:
    coment = await coment_sev.update_comet_like_unlike(
        coment_id=coment_id, user_id=user_id, type_rec=type_rec
    )
    if not coment:
        raise HTTPException(detail="Не найдено такой кометария ", status_code=404)
    return ComentResponse.from_orm(coment)


@coment_router.delete("/delete/{comnet_id}")
async def delete_coment(
    comnet_id: UUID, coment_sev: ComentService = Depends(get_comment_service)
) -> Dict[str, str]:
    coment = await coment_sev.delete_coment(comnet_id)
    if not coment:
        raise HTTPException(detail="Не найдено такой кометария ", status_code=404)
    return {"message": "Delete coment and db"}
