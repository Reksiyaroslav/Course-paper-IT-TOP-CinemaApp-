from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import Author
from sqlalchemy import select, or_, delete
from uuid import UUID


class AuthorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_author(self, data: dict):
        author = Author(**data)
        self.session.add(author)
        await self.session.commit()
        return author

    async def get_authors(self):
        relult = await self.session.execute(select(Author))
        author = relult.scalars().all()
        return author

    async def get_author_by_id(self, author_id):
        author = await self.session.get(Author, author_id)
        return author

    async def update_author(self, data: dict, author_id):
        author = await self.get_author_by_id(author_id=author_id)
        for key, values in data.items():
            if values is not None and hasattr(author, key):
                setattr(author, key, values)
        await self.session.commit()
        await self.session.refresh(author)
        return author

    async def delete_author(self, author_id) -> dict:
        smt = delete(Author).filter(Author.author_id == author_id)
        await self.session.execute(smt)
        await self.session.commit()
        return {"message": "Delete actor the db"}

    async def get_author_fistname_latname_pat(self, author_name: str) -> Author | None:
        smt = select(Author).where(
            (Author.fistname == author_name)
            | (Author.lastname == author_name)
            | (Author.patronymic == author_name)
        )
        relult = await self.session.execute(smt)
        author = relult.scalars().first()
        if not author:
            return None
        return author

    async def get_author_fistname_latname_pat_list(
        self, author_name: str, limit: int
    ) -> list[Author]:
        seareath_parametr = f"%{author_name}%"
        smt = select(Author).where(
            or_(
                Author.fistname.contains(seareath_parametr),
                Author.lastname.contains(seareath_parametr),
                Author.patronymic.contains(seareath_parametr),
            ).limit(limit)
        )
        relult = await self.session.execute(smt)
        authors = relult.scalars().all()
        return authors

    async def get_list_author_ids(self, author_ids: list[UUID]):
        smt = select(Author).where(Author.author_id.in_(author_ids))
        relut = await self.session.execute(smt)
        list_authors = relut.scalars().all()
        return list_authors
