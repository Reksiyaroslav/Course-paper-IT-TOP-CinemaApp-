from sqlalchemy import select, and_
from datetime import date, timedelta
import bcrypt
from fastapi import Depends
from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker
from random import randint
from uuid import UUID
from fastapi import HTTPException, status

from app.db.engine import get_session
from app.search_class.list_searhc import (
    list_blocked_text,
)
from app.enums.type_model import TypeModel
from app.enums.serach_fileld import SerachFiled

Confgi_dict = {
    "fistname": {"min_len": 3, "max_len": 50},
    "lastname": {"min_len": 3, "max_len": 50},
    "patronymic": {"min_len": 3, "max_len": 50},
    "title": {"min_len": 5, "max_len": 1000},
    "description": {"min_len": 20, "max_len": 4000},
    "type_film": {"min_len": 5, "max_len": 40},
    "country_name": {"min_len": 3, "max_len": 20},
}

SessionDep = Annotated[AsyncSession, Depends(get_session)]
faker = Faker()
YEARS_FILMS = 30
YEARS_ACTOR = 80


async def get_current_session():
    curern_month = date.today().month
    if curern_month in [12, 1, 2]:
        return 12, 2
    if curern_month in [3, 4, 5]:
        return 3, 5
    if curern_month in [6, 7, 8]:
        return 6, 8
    if curern_month in [9, 10, 11]:
        return 9, 11


async def is_name_title(model, session, name_filed, name_or_title_value) -> bool:
    smt = select(model).where(getattr(model, name_filed) == name_or_title_value)
    relut = await session.execute(smt)
    extit = relut.scalars().first() is None
    return extit


def generatao_bio() -> str:
    return faker.text(max_nb_chars=500)


def generatao_destripsion() -> str:
    return faker.text(max_nb_chars=200)


def generator_star() -> int:
    return randint(1, 5)


async def is_fistname_lastname(mode, session, dict_data):
    fields = SerachFiled.Name.value[:3]
    mas = [getattr(mode, field) == dict_data[field] for field in fields]
    smt = select(mode).where(and_(*mas))
    relut = await session.execute(smt)
    extit = relut.scalars().first() is None
    return extit


async def not_create_rating(
    model, session: AsyncSession, film_id: UUID, user_id: UUID
) -> bool:
    smt = select(model).where(and_(model.user_id == user_id, model.film_id == film_id))
    rating = await session.execute(statement=smt)
    return rating is None


async def validate_is_data_range(value: date, type_obj: str) -> bool:
    today = date.today()
    if type_obj == TypeModel.Film:
        min_date = today - timedelta(YEARS_FILMS * 365)
        if value > today or value < min_date:
            return False
    elif type_obj == TypeModel.Actor or TypeModel.Author:
        min_date = today - timedelta(YEARS_ACTOR * 365)
        if value > today or value < min_date:
            return False
    return True


async def validet_star_rating(dict: dict, filed_name: str) -> bool:
    if filed_name == SerachFiled.Rating.value[0]:
        if dict[filed_name] < 1 or dict[filed_name] > 10:
            return False
        return True
    return False


async def validet_text_coment(dict: dict, filed_name: str) -> bool:
    if filed_name not in dict:
        return False
    text_value = dict.get(filed_name)
    if text_value is None or not isinstance(text_value, str):
        return False
    if not text_value.strip():
        return False
    text_lower = text_value.lower().strip()
    for block_text in list_blocked_text:
        if block_text in text_lower:
            return False
    return True


def hath_password(password: str):
    password_byte = password.encode("utf-8")
    salf = bcrypt.gensalt()
    hash = bcrypt.hashpw(password_byte, salf)
    return hash.decode("utf-8")


def auth_password(password_user: str, password_api: str):
    password_api_byte = password_api.encode("utf-8")
    password_user_byte = password_user.encode("utf-8")
    return bcrypt.checkpw(
        password=password_api_byte, hashed_password=password_user_byte
    )


def len_fields(value_files: str, config_type: str) -> bool:
    config = Confgi_dict.get(config_type)
    if not config:
        return False
    if not value_files or not value_files.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Поля не могу быть пустыми"
        )
    clear_name_filed = value_files.strip()
    len_filen = len(clear_name_filed)
    min_len = config["min_len"]
    max_len = config["max_len"]
    if len_filen < min_len:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Поля не может быть меньше чем минальное{min_len} ",
        )
    if len_filen > max_len:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Поля не может быть больше чем  максимальное{max_len} ",
        )
    return True
