from typing import Dict, List
from fastapi import APIRouter, HTTPException,Query
from app.scheme.model_actor import ActorCreateRequest, ActorResponse, ActorUpdateRequest
from app.repositories.actors_repositorie import ActorRepository
from app.service.factory import get_service
from app.service.actor_service import ActorService
from app.utils.comon import SessionDep

from uuid import UUID

actor_router = APIRouter(prefix="/actor", tags=["Actor"])


@actor_router.post("/")
async def create_actor(
    data: ActorCreateRequest, async_session: SessionDep 
) -> ActorResponse:
    actor_servers = await get_service(ActorService, ActorRepository, async_session)
    actor = await actor_servers.create_model(data.dict())
    if not actor:
        raise HTTPException(status_code=401, detail="not create user")
    return ActorResponse.from_orm(actor)

@actor_router.get("s/")
async def get_actors(
    async_session: SessionDep,
) -> List[ActorResponse]:
    actor_sev = await get_service(ActorService, ActorRepository, async_session)
    actors = await actor_sev.get_models()
    return [ActorResponse.from_orm(actor) for actor in actors]


@actor_router.get("/{actor_id}")
async def get_actor_actor_id(
    actor_id: UUID, async_session: SessionDep
) -> ActorResponse:
    actor_sev = await get_service(ActorService, ActorRepository, async_session)
    actor = await actor_sev.get_model(actor_id)
    if not actor:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return ActorResponse.from_orm(actor)


@actor_router.get("/name_actor/{fistname_latname_pat}")
async def get_name_actor(
    fistname_latname_pat: str, async_session: SessionDep
):
    actor_sev = await get_service(ActorService, ActorRepository, async_session)
    actor = await actor_sev.get_fistname_lastname_pat(fistname_latname_pat)
    if not actor:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return ActorResponse.from_orm(actor)


@actor_router.get("/name_actors/{fistname_latname_pat}")
async def get_name_actors(
    fistname_latname_pat: str, async_session: SessionDep
) -> ActorResponse:
    actor_sev = await get_service(ActorService, ActorRepository, async_session)
    actor = await actor_sev.get_serahc_name_list(fistname_latname_pat)
    if not actor:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return ActorResponse.from_orm(actor)


@actor_router.put("/update/{actor_id}")
async def update_actor(
    data: ActorUpdateRequest,
    actor_id: UUID,
    async_session:  SessionDep
) -> ActorResponse:
    actor_servers = await get_service(ActorService, ActorRepository, async_session)
    actor = await actor_servers.update_model(actor_id, data.dict())
    if not actor:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return ActorResponse.from_orm(actor)


@actor_router.delete("/delete/{actor_id}")
async def delete_actor(
    actor_id: UUID, async_session:SessionDep
) -> Dict[str, str]:
    actor_sev = await get_service(ActorService, ActorRepository, async_session)
    actor = await actor_sev.delete_model(actor_id)
    if not actor:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return {"message": "Delete actor and db"}
