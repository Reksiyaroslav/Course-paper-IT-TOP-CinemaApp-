from typing import Dict, List
from fastapi import APIRouter, HTTPException
from app.scheme.actor.model_actor import ActorCreateRequest, ActorResponse, ActorUpdateRequest
from app.utils.comon import  Depends
from app.utils.depencines import ActorService, get_actor_service
from uuid import UUID

actor_router = APIRouter(prefix="/actor", tags=["Actor"])


@actor_router.post("/")
async def create_actor(
    data: ActorCreateRequest, actor_service: ActorService = Depends(get_actor_service)
) -> ActorResponse:
    actor = await actor_service.create_actor(data.model_dump())
    if not actor:
        raise HTTPException(status_code=401, detail="not create actor")
    return ActorResponse.from_orm(actor)


@actor_router.get("s/")
async def get_actors(
    actor_service: ActorService = Depends(get_actor_service),
) -> List[ActorResponse]:
    actors = await actor_service.get_actor_list()
    return [ActorResponse.from_orm(actor) for actor in actors]


@actor_router.get("profile/{actor_id}")
async def get_actor_actor_id(
    actor_id: UUID, actor_service: ActorService = Depends(get_actor_service)
) -> ActorResponse:
    actor = await actor_service.get_actor_by_id(actor_id)
    if not actor:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return ActorResponse.from_orm(actor)


@actor_router.get("/name_actors/{fistname_latname_pat}")
async def get_name_actors(
    fistname_latname_pat: str, actor_service: ActorService = Depends(get_actor_service)
) -> List[ActorResponse]:
    actors = await actor_service.get_serahc_name_list(fistname_latname_pat)
    if not actors:
        raise HTTPException(detail="Не найдено такой актёров", status_code=404)
    return [ActorResponse.from_orm(actor) for actor in actors]


@actor_router.put("/update/{actor_id}")
async def update_actor(
    data: ActorUpdateRequest,
    actor_id: UUID,
    actor_service: ActorService = Depends(get_actor_service),
) -> ActorResponse:
    actor = await actor_service.update_actor(actor_id=actor_id, data=data.dict())
    if not actor:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return ActorResponse.from_orm(actor)


@actor_router.delete("/delete/{actor_id}")
async def delete_actor(
    actor_id: UUID, actor_service: ActorService = Depends(get_actor_service)
) -> Dict[str, str]:
    actor = await actor_service.delete_actor(actor_id)
    if not actor:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return {"message": "Delete actor and db"}
