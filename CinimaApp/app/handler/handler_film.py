from litestar import Controller,get,post,delete,put,Router
from litestar.params import Dependency
from app.model.model_film import FilmCreateRequest,FilmResponse,FilmUpdateRequest,FilmlListResponse,AddAuthorFilsmResponse,AddActorFilsmResponse
from app.repositories.films_repositorie import FilmRepository
from sqlalchemy.ext.asyncio import AsyncSession 
from uuid import UUID
from litestar.exceptions import HTTPException
from app.auth.auth import jwt_auth
class FilmControlle(Controller):
    path ="/film"
    tags =["Film"]
    security =[]
    @post()
    async def create_films(self,data:FilmCreateRequest,async_session:AsyncSession=Dependency())->FilmResponse:
        film_repo   = FilmRepository(async_session) 
        film = await film_repo.create(data.dict())
        return FilmResponse.from_orm(film)
    @post("/id/{film_id:uuid}/actor/{actor_id:uuid}")
    async def add_film_actor(self,film_id:UUID,actor_id:UUID,async_session:AsyncSession=Dependency())->FilmResponse:
        film_repo = FilmRepository(async_session)
        film = await film_repo.add_actor(actor_id,film_id)
        return FilmResponse.from_orm(film)
    @post("/id/{film_id:uuid}/actors/")
    async def add_film_actorlist(self,film_id:UUID,data:AddActorFilsmResponse,async_session:AsyncSession=Dependency())->FilmResponse:
        film_repo = FilmRepository(async_session)
        film = await film_repo.add_list_actor_id(data.actor_ids,film_id)
        return FilmResponse.from_orm(film)
    @post("/id/{film_id:uuid}/authors/")
    async def add_film_autorlist(self,film_id:UUID,data:AddAuthorFilsmResponse,async_session:AsyncSession=Dependency())->FilmResponse:
        film_repo = FilmRepository(async_session)
        film = await film_repo.add_list_author_id(data.author_ids,film_id)
        return FilmResponse.from_orm(film)
    @get()
    async def get_filmlist(self,async_session:AsyncSession=Dependency())->FilmlListResponse:
        film_repo = FilmRepository(async_session)
        films = await film_repo.get_list_model()
        films_rensopnses = [FilmResponse.from_orm(film) for film in films ]
        return FilmlListResponse(films=films_rensopnses)
    @get("id/{film_id:uuid}")
    async def get_film_id(self,film_id:UUID,async_session:AsyncSession=Dependency())->FilmResponse:
        film_repo = FilmRepository(async_session)
        film = await film_repo.get_model_id(film_id)
        return FilmResponse.from_orm(film)
    @get("titel/{film_titel:str}")
    async def get_filim_titel(self,film_titel:str,async_session:AsyncSession=Dependency())->FilmResponse:
        film_repo = FilmRepository(async_session)
        film = await film_repo.get_film_title(film_titel)
        if not film:
            raise HTTPException("Not film" ,status_code=404)
        return FilmResponse.from_orm(film)
    @put("id/{film_id:uuid}" ,summary="Update film")
    async def update_film(self,film_id:UUID, data:FilmUpdateRequest ,async_session:AsyncSession=Dependency())->FilmResponse:
        film_repo   = FilmRepository(async_session)
        film = await film_repo.update_model(film_id,data.dict(exclude_unset=True))
        if not film:
            raise HTTPException(status_code=404,detail="Not film")
        return FilmResponse.from_orm(film)
    @delete("id/{film_id:uuid}",status_code=200)
    async def delete_film(self,film_id:UUID,async_session:AsyncSession)->dict[str,str]:
        film_repo = FilmRepository(async_session)
        film = await film_repo.model_delete(film_id)
        if not film:
            raise HTTPException("Not film" ,status_code=404)
        return{"detali":"delete Film db"}
    
        


