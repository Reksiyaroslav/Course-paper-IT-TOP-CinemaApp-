from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.model.model_db import User, Coment, RatingFilm
from app.utils.comon import hath_password, auth_password
from uuid import UUID
from app.repositories.repostoried import ModelRepository
from app.repositories.films_repositorie import FilmRepository


class UserRepository(ModelRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=User)

    async def create(self, data):
        if "password" in data:
            data["password"] = hath_password(data["password"])
        return await super().create(data)

    async def update_model(self, model_id, data):
        if "password" in data and data["password"] != None:
            data["password"] = hath_password(data["password"])
        return await super().update_model(model_id, data)

    async def get_name(self, username: str) -> User:
        smt = select(User).where(User.username == username)
        result = await self.session.execute(smt)
        user = result.scalars().first()
        return user

    async def get_username_password(self, username: str, password: str) -> User:

        smt = select(User).where(User.username == username)
        result = await self.session.execute(smt)
        user = result.scalars().first()
        if not user:
            return None

        if auth_password(user.password, password):
            return user
        return None

    """async def add_frinde(self,user_id:UUID,friend_id:UUID):
        user = await self.get_model_id(user_id)
        friend = await self.get_model_id(friend_id)
        if not user:
            raise ValueError("Нет такого пользователя ")
        if not friend:
            raise ValueError("Нет такого друга ")
        if friend not in user.friends:
            user.friends.append(friend)
            await self.session.commit()
            await self.session.refresh(user)
        else:
            raise ValueError("Пользователь уже есть в друзьях")
        return user"""

    async def add_licefilm(self, user_id: UUID, film_id: UUID):
        film_repo = FilmRepository(self.session)
        user = await self.get_model_id(user_id)
        film = await film_repo.get_model_id(film_id)
        if not user:
            raise ValueError("Нет такого пользователя")
        if not film:
            raise ValueError("Нет такого фильма")
        if film not in user.likefilms:
            user.likefilms.append(film)
            await self.session.commit()
            await self.session.refresh(user)
        else:
            raise ValueError("Уже есть в списке пользователя")
        return user

    async def get_list_licefilm(self, user_id: UUID):

        film_repo = FilmRepository(self.session)
        user = await self.get_model_id(user_id)
        if not user:
            raise ValueError("Нет такого пользователя")
        film_ids = [likefilm.id for likefilm in user.likefilms]
        films = await film_repo.get_film_film_ids(film_ids)
        return films

    async def add_coment_user(self, user_id: UUID, coment: Coment):
        user = await self.get_model_id(user_id)
        if user:
            user.coment_users.append(coment)
            await self.session.commit()
            await self.session.refresh(user)

    async def add_ratingfilm_user(self, user_id: UUID, ratingfilm: RatingFilm):
        user = await self.get_model_id(user_id)
        if user:
            user.rating_users.append(ratingfilm)
            await self.session.commit()
            await self.session.refresh(user)
