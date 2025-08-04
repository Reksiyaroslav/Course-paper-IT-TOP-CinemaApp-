from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import Film, User, Coment
from sqlalchemy import select, delete
from app.repositories.repostoried import ModelRepository
import uuid
from app.repositories.users_repositorie import UserRepository
from app.repositories.films_repositorie import FilmRepository


class ComentRepository(ModelRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Coment)

    async def create_coment(self, data):
        coment = Coment(
            description=data["description"],
            countheart=data["countheart"],
            countdemon=data["countdemon"],
        )

        film_repo = FilmRepository(self.session)
        user_repo = UserRepository(self.session)

        film = await film_repo.get_model_id(data["film_id"])
        if film is None:
            raise ValueError(f"User with id {data['film_id']} not found")
        user = await user_repo.get_model_id(data["user_id"])
        if user is None:
            raise ValueError(f"User with id {data['user_id']} not found")
        coment.films.append(film)
        coment.users.append(user)

        await self.session.commit()
        await self.session.refresh(coment)
        return coment

    async def list_film_coments(self, film_id: uuid.UUID):
        stmt = select(Coment).join(Coment.films).where(Film.id == film_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_user_coments(self, user_id: uuid.UUID):
        stmt = select(Coment).join(Coment.users).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
