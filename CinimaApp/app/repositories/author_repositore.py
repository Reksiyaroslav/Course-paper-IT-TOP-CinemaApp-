from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model_db.model_db import Author
from sqlalchemy import select, delete, update
from uuid import UUID
from app.repositories.repostoried import ModelRepository


class AuthorRepository(ModelRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Author)

    async def get_author_fistname_latname_pat(self, author_name: str) -> Author:
        smt = select(Author).where(
            (Author.fistName == author_name)
            | (Author.lastName == author_name)
            | (Author.patronymic == author_name)
        )
        relult = await self.session.execute(smt)
        author = relult.scalars().first()
        return author

    async def get_author_fistname_latname_pat_list(self, author_name: str) -> Author:
        smt = select(Author).where(
            (Author.fistname == author_name)
            | (Author.lastname == author_name)
            | (Author.patronymic == author_name)
        )
        relult = await self.session.execute(smt)
        author = relult.scalars().all()
        return author

    async def get_list_author_ids(self, author_ids: UUID):
        smt = select(Author).where(Author.id.in_(author_ids))
        relut = await self.session.execute(smt)
        list_authors = relut.scalars().all()
        return list_authors
