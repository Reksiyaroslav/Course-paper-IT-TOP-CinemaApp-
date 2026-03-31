from app.service.actor_service import ActorService
from app.service.author_service import AuthorService
from app.service.coment_service import ComentService
from app.service.ratingfilms_service import RatingFilmService
from app.service.film_service import FilmService
from app.service.user_service import UserService
from app.service.country_service import CountryService
from app.utils.comon import SessionDep


async def get_user_service(async_session: SessionDep) -> UserService:
    return UserService(async_session)


async def get_film_service(async_session: SessionDep) -> FilmService:
    return FilmService(session=async_session)


async def get_actor_service(async_session: SessionDep) -> ActorService:
    return ActorService(async_session)


async def get_author_service(async_session: SessionDep) -> AuthorService:
    return AuthorService(async_session)


async def get_comment_service(async_session: SessionDep) -> ComentService:
    return ComentService(async_session)


async def get_rating_service(async_session: SessionDep) -> RatingFilmService:
    return RatingFilmService(async_session)


async def get_country_service(async_session: SessionDep) -> CountryService:
    return CountryService(async_session)
