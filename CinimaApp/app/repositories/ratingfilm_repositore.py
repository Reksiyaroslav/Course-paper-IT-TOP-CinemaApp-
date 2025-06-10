from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model_db.model_db import RatingFilm
from sqlalchemy import select,delete,update
from uuid import UUID
from app.repositories.repostoried import ModelRepository
class RatingFilmRepository(ModelRepository):
    def __init__(self,session:AsyncSession):
        super().__init__(session=session,model=RatingFilm)
   
    async def add_upadate_rating_user_and_film(self,film_id:UUID,user_id:UUID,rating:int):
        async with self.session.begin():
            smt = select(RatingFilm).where(RatingFilm.film_id ==film_id , RatingFilm.user_id==user_id)
            relult = await self.session.execute(smt)
            exitst = relult.scalars().first()
        
            if exitst:
                exitst.rating =rating
                rating_obj = exitst.rating   
            else:
                rating_obj = RatingFilm(user_id=user_id,film_id=film_id,rating=rating)
                self.session.add(rating_obj)
            await self.session.refresh(rating_obj)
            return rating_obj
    async def get_list_film_rating(self,film_id:UUID):
        smt = select(RatingFilm).where(RatingFilm.film_id== film_id)
        relut = await self.session.execute(smt)
        return relut.scalars().all() 
    async def get_list_user_rating(self,user_id:UUID):
        smt = select(RatingFilm).where(RatingFilm.user_id== user_id)
        relut = await self.session.execute(smt)
        return relut.scalars().all()   
    async def get_user_film_rating(self,film_id:UUID,user_id:UUID):
        smt = select(RatingFilm).where(RatingFilm.film_id==film_id,RatingFilm.user_id == user_id)  
        relut = await self.session.execute(smt)
        return relut.scalars().first()   