from fastapi import Request, Depends, HTTPException
from datetime import date
from app.utils.depencines import get_user_service, UserService
from app.scheme.user.model_user import UserResponse
from app.utils.depencines import (
    CountryService,
    FilmService,
    ActorService,
    AuthorService,
)


async def get_curen_user(
    request: Request, user_service: UserService = Depends(get_user_service)
) -> UserResponse | None:
    try:
        user_id = request.session.get("user_id")
        if not user_id:
            return None
        user = await user_service.get_user_by_id(user_id)
        print(user)
        return user
    except Exception:
        return None


async def get_data_form(
    country_service: CountryService,
    film_service: FilmService,
    actor_service: ActorService,
    author_service: AuthorService,
):
    data = {
        "countrys": [],
        "types_film": [],
        "actors": [],
        "authors": [],
    }
    if country_service:
        country_relult = await country_service.get_countrys()
        coyntrys = country_relult.countrys
        data["countrys"] = coyntrys
    if actor_service:
        actor_relult = await actor_service.get_actor_list()
        actors = actor_relult.actors
        data["actors"] = actors
    if author_service:
        author_relult = await author_service.get_authors()
        authors = author_relult.author
        data["authors"] = authors
    if film_service:
        type_film_relult = await film_service.get_types_film()
        types_film = type_film_relult.types_film
        data["types_film"] = types_film
    return data


def parse_data_or_none(date_str: str, field_name: str = "date"):
    clean_date_str = date_str.strip()
    if not date_str or not clean_date_str:
        return None
    try:
        return date.fromisoformat(clean_date_str)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Неверный формат '{field_name}'. Ожидается YYYY-MM-DD.",
        )
