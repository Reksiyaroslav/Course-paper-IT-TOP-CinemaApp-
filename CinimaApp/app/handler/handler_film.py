from litestar import Controller, get, post, delete, put, Router
from app.model.model_film import (
    FilmCreateRequest,
    FilmResponse,
    FilmUpdateRequest,
    FilmlListResponse,
    AddAuthorFilsmResponse,
    AddActorFilsmResponse,
)
from app.model.model_actor import ActorResponse
from app.model.model_author import AuthorResponse
from app.repositories.films_repositorie import FilmRepository
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from litestar.exceptions import HTTPException
from app.service.factory import get_service
from app.service.film_service import FilmService


class FilmControlle(Controller):
    path = "/film"
    tags = ["Film"]
    security = []

    @post()
    async def create_films(
        self, data: FilmCreateRequest, async_session: AsyncSession
    ) -> FilmResponse:
        film_service = get_service(FilmService, FilmRepository, async_session)
        film = await film_service.create_model(data.dict())
        return FilmResponse.from_orm(film)

    @post("/id/{film_id:uuid}/actors/")
    async def add_film_actorlist(
        self, film_id: UUID, data: AddActorFilsmResponse, async_session: AsyncSession
    ) -> FilmResponse:
        film_service = get_service(FilmService, FilmRepository, async_session)
        film = await film_service.add_actors_film_model(data.dict(), film_id)
        return FilmResponse.from_orm(film)

    @post("/id/{film_id:uuid}/authors/")
    async def add_film_autorlist(
        self, film_id: UUID, data: AddAuthorFilsmResponse, async_session: AsyncSession
    ) -> FilmResponse:
        film_service = get_service(FilmService, FilmRepository, async_session)
        film = await film_service.add_authors_film_model(data.dict(), film_id)
        return FilmResponse.from_orm(film)

    @get()
    async def get_filmlist(self, async_session: AsyncSession) -> FilmlListResponse:
        film_service = get_service(FilmService, FilmRepository, async_session)
        films = await film_service.get_models()
        films_rensopnses = [FilmResponse.from_orm(film) for film in films]
        return FilmlListResponse(films=films_rensopnses)

    @get("id/{film_id:uuid}")
    async def get_film_id(
        self, film_id: UUID, async_session: AsyncSession
    ) -> FilmResponse:
        film_service = get_service(FilmService, FilmRepository, async_session)
        film = await film_service.get_model(film_id)
        return FilmResponse.from_orm(film)

    @get("id/{film_id:uuid}/actors")
    async def get_actor_list(
        self, film_id: UUID, async_session: AsyncSession
    ) -> list[ActorResponse]:
        film_service = get_service(FilmService, FilmRepository, async_session)
        actors = await film_service.get_list_actor(film_id)
        return [ActorResponse.from_orm(actor) for actor in actors]

    @get("id/{film_id:uuid}/authors")
    async def get_author_list(
        self, film_id: UUID, async_session: AsyncSession
    ) -> list[AuthorResponse]:
        film_service = get_service(FilmService, FilmRepository, async_session)
        authors = await film_service.get_list_author(film_id)
        return [AuthorResponse.from_orm(author) for author in authors]

    @get("titel/{film_titel:str}")
    async def get_filim_titel(
        self, film_titel: str, async_session: AsyncSession
    ) -> FilmlListResponse:
        film_service = get_service(FilmService, FilmRepository, async_session)
        films = await film_service.get_film_title(film_titel)
        films_rensopnses = [FilmResponse.from_orm(film) for film in films]
        if not films_rensopnses:
            raise HTTPException("Not film", status_code=404)
        return FilmlListResponse.from_orm(film=films_rensopnses)

    @put("id/{film_id:uuid}", summary="Update film")
    async def update_film(
        self, film_id: UUID, data: FilmUpdateRequest, async_session: AsyncSession
    ) -> FilmResponse:
        film_service = get_service(FilmService, FilmRepository, async_session)
        film = await film_service.update_model(film_id, data.dict())
        if not film:
            raise HTTPException(status_code=404, detail="Not film")
        return FilmResponse.from_orm(film)

    @delete("id/{film_id:uuid}", status_code=200)
    async def delete_film(
        self, film_id: UUID, async_session: AsyncSession
    ) -> dict[str, str]:
        film_service = get_service(FilmService, FilmRepository, async_session)
        film = await film_service.delete_model(film_id)
        if not film:
            raise HTTPException("Not film", status_code=404)
        return {"detali": "delete Film db"}
