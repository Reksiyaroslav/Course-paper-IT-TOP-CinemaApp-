import asyncio
from faker import Faker
import random
from app.db.model.model_db import (
    Film,
    User,
    Actor,
    Author,
    user_film,
    author_ciema,
    film_actor,
    Base,
)
from app.db.engine import get_session, enigine
from sqlalchemy import select, func
import bcrypt
from app.utils.comon import faker


async def init_db():
    async with enigine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
        print("Таблицы созданы или уже существуют")


async def seend_database():
    await init_db()
    async for session in get_session():
        actors = []
        users = []
        authors = []
        films = []
        # Созданрие актера
        for _ in range(1, 50):
            actor = Actor(
                fistname=faker.first_name(),
                lastname=faker.last_name(),
                patronymic=faker.first_name(),
                star=random.randint(0, 10),
                birth_date=faker.date_of_birth(minimum_age=18, maximum_age=80),
            )
            actors.append(actor)
        session.add_all(actors)
        await session.commit()
        # Создание автора
        for _ in range(0, 30):
            author = Author(
                fistname=faker.first_name(),
                lastname=faker.last_name(),
                patronymic=faker.first_name(),
                bio=faker.text(max_nb_chars=200),
                birth_date=faker.date_of_birth(minimum_age=18, maximum_age=80),
            )
            authors.append(author)
        session.add_all(authors)
        await session.commit()
        # Создание пользователя
        for _ in range(1, 4):
            password = faker.password(length=12).encode("utf-8")
            salf = bcrypt.gensalt()
            hath = bcrypt.hashpw(password, salf)
            hath.decode("utf-8")
            user = User(
                password=hath.decode("utf-8"),
                email=faker.email(),
                username=faker.user_name(),
            )
            users.append(user)
        session.add_all(users)
        await session.commit()
        # Создание фильмов
        for _ in range(1, 100):
            film = Film(
                title=faker.catch_phrase(),
                description=faker.text(max_nb_chars=500),
                release_date=faker.date_between(start_date="-30y", end_date="today"),
                estimation=random.randint(1, 10),
                path_image="../images/cat.jpg",
            )
            films.append(film)
        session.add_all(films)
        await session.commit()
        for film_obj in films:
            select_actor = random.sample(actors, random.randint(1, 4))
            for actor in select_actor:
                smt = film_actor.insert().values(film_id=film_obj.id, actor_id=actor.id)
                await session.execute(smt)
            select_auhtor = random.sample(authors, random.randint(1, 3))
            for author in select_auhtor:
                smt = author_ciema.insert().values(
                    film_id=film_obj.id, author_id=author.id
                )
                await session.execute(smt)
        await session.commit()
        for user in users:
            num_lice = random.randint(0, 10)
            if num_lice > 0 and films:
                like_film = random.sample(films, min(num_lice, len(films)))
            for film_obj in like_film:
                smt = user_film.insert().values(user_id=user.id, film_id=film_obj.id)
                await session.execute(smt)
        await session.commit()
    actors_count = await session.scalar(select(func.count(Actor.id)))
    users_count = await session.scalar(select(func.count(User.id)))
    films_count = await session.scalar(select(func.count(Film.id)))

    print(
        f"База заполнена! Актеры: {actors_count}, Фильмы: {films_count}, Пользователи: {users_count}"
    )


if __name__ == "__main__":
    asyncio.run(seend_database())
