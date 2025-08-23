from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import Author
from sqlalchemy import select, delete, update,or_
from uuid import UUID
from app.repositories.repostoried import ModelRepository


class AuthorRepository(ModelRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Author)
    
    async def get_author_fistname_latname_pat(self, author_name: str) -> Author:
        smt = select(Author).where(
            (Author.fistname == author_name)
            | (Author.lastname == author_name)
            | (Author.patronymic == author_name)
        )
        relult = await self.session.execute(smt)
        author = relult.scalars().first()
        return author

    async def get_author_fistname_latname_pat_list(self, author_name: str,limit:int) -> Author:
        seareath_parametr = f"%{author_name}%"
        smt = select(Author).where(
            or_(
            (Author.fistname.ilike(seareath_parametr))
            (Author.lastname.ilike(seareath_parametr))
            (Author.patronymic.ilike(seareath_parametr))
            )
        ).limit(limit)
        relult = await self.session.execute(smt)
        author = relult.scalars().all()
        return author

    async def get_list_author_ids(self, author_ids: UUID):
        smt = select(Author).where(Author.id.in_(author_ids))
        relut = await self.session.execute(smt)
        list_authors = relut.scalars().all()
        return list_authors
