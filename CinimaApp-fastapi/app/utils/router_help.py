from fastapi import Request, Depends, HTTPException
from datetime import date
from urllib.parse import urlparse, quote
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


def parse_data_or_none(date_str: str, field_name: str = "date"):

    if not date_str or not date_str.strip():
        return None
    try:
        clean_date_str = date_str.strip()
        return date.fromisoformat(clean_date_str)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Неверный формат '{field_name}'. Ожидается YYYY-MM-DD.",
        )


def clean_url_redirect(error_message: str, base_url: str, error_met: str):
    parse = urlparse(base_url)
    clean_path = parse.path
    encode_message = quote(error_message, safe=" ")
    return f"{clean_path}?{error_met}={encode_message}"
