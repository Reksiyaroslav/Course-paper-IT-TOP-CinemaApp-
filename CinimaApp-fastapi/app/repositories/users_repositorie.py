from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.db.model.model_db import User, Coment, RatingFilm, Film, user_film_like
from app.utils.comon import hath_password, auth_password
from sqlalchemy.orm import selectinload
from uuid import UUID
from app.repositories.films_repositorie import FilmRepository


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, data: dict) -> User | None:
        try:
            if "password" in data:
                data["password"] = hath_password(data["password"])
            db_user = User(**data)
            self.session.add(db_user)
            await self.session.commit()
            return db_user
        except SQLAlchemyError as e:
            await self.session.rollback()
            print("Error", e._message)
            return None

    async def get_list_users(self):
        try:
            smt = select(User).options(
                selectinload(User.coments),
                selectinload(User.rating_users),
                selectinload(User.likefilms),
                selectinload(User.reviews),
            )
            relult = await self.session.execute(smt)
            user = relult.scalars().unique().all()
            return user
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        try:
            smt = (
                select(User)
                .options(
                    selectinload(User.coments),
                    selectinload(User.rating_users),
                    selectinload(User.likefilms),
                    selectinload(User.reviews),
                )
                .filter(User.user_id == user_id)
            )
            relult = await self.session.execute(smt)
            user = relult.scalars().first()
            return user
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise

    async def update_user(self, user_id: UUID, data: dict) -> User | None:
        if "password" in data and data["password"] != None:
            data["password"] = hath_password(data["password"])
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        for key, values in data.items():
            if values is not None and hasattr(user, key):
                setattr(user, key, values)
        await self.session.commit()
        await self.session.refresh(user)
        update_user = await self.get_user_by_id(user_id)
        return update_user

    async def delete_user(self, user_id: UUID) -> bool:
        try:
            smt = delete(User).where(User.user_id == user_id)
            await self.session.execute(smt)
            await self.session.commit()
            return True
        except Exception:
            await self.session.rollback()
            return False

    async def get_name(self, username: str) -> User | None:
        smt = select(User).where(User.username == username)
        result = await self.session.execute(smt)
        user = result.scalars().first()
        if not user:
            return None
        return user

    async def update_datanow(self, user_id: UUID):
        user = await self.get_user_by_id(user_id=user_id)
        user.datetimenow = datetime.today()
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_username_password(self, data: dict) -> User | None:
        email: str = data.get("email")
        password: str = data.get("password")
        smt = select(User).where(or_(User.email == email, User.username == email))
        result = await self.session.execute(smt)
        user = result.scalars().first()
        if not user:
            return None
        if auth_password(password_user=user.password, password_api=password):
            user = await self.update_datanow(user_id=user.user_id)
            return user
        return None

    async def set_user_role(self, user_id: UUID, role_user: str):
        user = await self.get_user_by_id(user_id=user_id)
        if not user:
            return None
        if user.role_user == role_user:
            return user
        user.role_user = role_user
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_block_users(self) -> list[User]:
        smt = select(User.user_id, User.username, User.email)
        result = await self.session.execute(smt)
        rows = result.all()
        users = []
        for row in rows:
            user = User()
            user.user_id = row[0]
            user.username = row[1]
            user.email = row[2]
            users.append(user)
        return users

    async def add_licefilm(self, user_id: UUID, film: Film) -> User:
        user = await self.get_user_by_id(user_id)
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

    async def delete_likefilm(self, user_id: UUID, film_id: UUID):
        try:
            smt = delete(user_film_like).where(
                and_(
                    user_film_like.c.user_id == user_id,
                    user_film_like.c.film_id == film_id,
                )
            )
            relult = await self.session.execute(smt)
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            print(e._message)
            await self.session.rollback()
            return False

    async def get_list_licefilm(self, user_id: UUID):
        film_repo = FilmRepository(self.session)
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("Нет такого пользователя")
        film_ids = [likefilm.film_id for likefilm in user.likefilms]
        films = await film_repo.get_film_film_ids(film_ids)
        return films

    async def add_coment_user(self, user_id: UUID, coment: Coment) -> None:
        user = await self.get_user_by_id(user_id)
        if user:
            user.coments.append(coment)
            await self.session.commit()
            await self.session.refresh(user)

    async def add_ratingfilm_user(self, user_id: UUID, ratingfilm: RatingFilm) -> None:
        user = await self.get_user_by_id(user_id)
        if user:
            user.rating_users.append(ratingfilm)
            await self.session.commit()
            await self.session.refresh(user)
