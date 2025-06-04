from litestar import get ,Controller,post,put,delete
from litestar.params import Dependency
from app.repositories.actors_repositorie import ActorRepository
from app.model.model_actor import ActorResponse,ActorCreateRequest,ActorUpdateRequest,ActorListResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from litestar.exceptions import HTTPException
from typing import Dict
class ActorControlle(Controller):
    path ="/actor"
    tags =["Actor"]
    security =[]
    @post()
    async def create_actor(self,data:ActorCreateRequest,async_session:AsyncSession =Dependency())->ActorResponse:
        actor_repo = ActorRepository(async_session)
        actor = await actor_repo.create(data.dict())
        return ActorResponse.from_orm(actor)
    @get()
    async def get_listactor(self,async_session:AsyncSession =Dependency())->ActorListResponse:
        actor_repo = ActorRepository(async_session)
        actors = await actor_repo.get_list_model()
        list_rensponse = [ActorResponse.from_orm(actor) for actor in actors]
        return ActorListResponse(actors= list_rensponse)
    @get("/{actor_fistname_or_lastname_or_patronymic:str}")
    async def get_actor_name(self,actor_fistname_or_lastname_or_patronymic:str,async_session:AsyncSession =Dependency())->list[ActorResponse]:
        actor_repo = ActorRepository(async_session)
        actor = await actor_repo.get_actorname(actor_fistname_or_lastname_or_patronymic)
        return  ActorResponse.from_orm(actor)
    @put("id/{actor_id:uuid}" ,summary="Update film")
    async def update_user(self,actor_id:UUID, data:ActorUpdateRequest ,async_session:AsyncSession=Dependency())->ActorResponse:
        actor_repo   = ActorRepository(async_session)
        actor = await actor_repo.update_model(actor_id,data.dict(exclude_unset=True))
        if not actor:
            raise HTTPException(status_code=404,detail="Not author")
        return ActorResponse.from_orm(actor)
    @delete("/{actor_id:uuid}",status_code=200)
    async def delete_actor(self,actor_id:UUID,async_session:AsyncSession =Dependency())->Dict[str,str]:
        actor_repo = ActorRepository(async_session)
        deleted = await actor_repo.model_delete(actor_id)
        if not deleted:
            raise HTTPException("Not found actor",status_code=404)
        return {"detail": "Actor deleted successfully"}

