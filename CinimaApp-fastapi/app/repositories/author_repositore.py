from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import Author, Country
from sqlalchemy import select, or_, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID


class AuthorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_author(self, data: dict) -> Author | None:
        "Создание автора"
        try:
            author = Author(**data)
            self.session.add(author)
            await self.session.commit()
            await self.session.refresh(author)
            return author
        except SQLAlchemyError as e:
            await self.session.rollback()
            print("Error create author " + e)
            return None

    async def get_authors(self) -> list[Author]:
        "Получения author"
        try:
            relult = await self.session.execute(select(Author))
            author = relult.scalars().all()
            return author
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(e)
            raise

    async def get_author_by_id(self, author_id):
        "Получения кортеного автора по id"
        smt = (
            select(Author)
            .options(selectinload(Author.films_authored), selectinload(Author.country))
            .where(Author.author_id == author_id)
        )
        relult = await self.session.execute(smt)
        author = relult.scalars().first()
        return author

    async def add_country(self, author_id: UUID, country_id: UUID):
        author = await self.get_author_by_id(author_id=author_id)
        if not author:
            return None
        smt = select(Country).where(Country.country_id == country_id)
        relut = await self.session.execute(smt)
        country = relut.scalars().first()
        if not country:
            return author
        author.country = country
        author.country_id = country.country_id
        await self.session.commit()
        await self.session.refresh(author)
        return author

    async def set_country(self, author_id: UUID, country_id: UUID):
        author = await self.get_author_by_id(author_id=author_id)
        if not author:
            return None
        smt = select(Country).where(Country.country_id == country_id)
        relut = await self.session.execute(smt)
        country = relut.scalars().first()
        if not country:
            return author
        if country.country_id == author.country_id:
            return author
        author.country = country
        author.country_id = country.country_id
        await self.session.commit()
        await self.session.refresh(author)
        return author

    async def update_author(self, data: dict, author_id) -> Author:
        "Обновления автора"
        author = await self.get_author_by_id(author_id=author_id)
        if not author:
            return None
        for key, values in data.items():
            if values is not None and hasattr(author, key):
                setattr(author, key, values)
        await self.session.commit()
        await self.session.refresh(author)
        return author

    async def delete_author(self, author_id) -> bool:
        "Удаления author"
        try:
            smt = delete(Author).filter(Author.author_id == author_id)
            relult = await self.session.execute(smt)
            await self.session.commit()
            return True
        except Exception as e:
            print(str(e))
            await self.session.rollback()
            return False

    async def get_author_fistname_latname_pat_list(
        self, author_name: str
    ) -> list[Author]:
        "Получения актеров по имени фамилиме которые есть часть текста"
        seareath_parametr = f"%{author_name}%"
        smt = select(Author).where(
            or_(
                Author.fistname.contains(seareath_parametr),
                Author.lastname.contains(seareath_parametr),
                Author.patronymic.contains(seareath_parametr),
            )
        )
        relult = await self.session.execute(smt)
        authors = relult.scalars().all()
        return authors

    async def get_list_author_ids(self, author_ids: list[UUID]) -> list[Author]:
        smt = select(Author).where(Author.author_id.in_(author_ids))
        relut = await self.session.execute(smt)
        list_authors = relut.scalars().all()
        return list_authors
