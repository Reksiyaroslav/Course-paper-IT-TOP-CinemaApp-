from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model_db.model_db  import Film
from sqlalchemy import select,delete,update
from uuid import UUID
from app.repositories.actors_repositorie import ActorRepository
from app.repositories.repostoried import ModelRepository
from app.repositories.author_repositore import AuthorRepository
class FilmRepository(ModelRepository):
    def __init__(self,session:AsyncSession):
        super().__init__(session,model=Film)
        
    async def add_actor(self,actor_id:UUID ,film_id:UUID)->Film|None:
        film = await self.get_model_id(film_id)
        if not film :
            return None 
        actor_repo= ActorRepository(self.session)
        actor =   await actor_repo.get_model_id(actor_id)
        if not any(a.id == actor_id for a in film.actors) :

            film.actors.append(actor)
        await self.session.commit()
        await self.session.refresh(film)
        return film
    async def add_author(self,author_id:UUID ,film_id:UUID)->Film|None:
        film = await self.get_model_id(film_id)
        if not film :
            return None 
        author_repo= AuthorRepository(self.session)
        author =   await author_repo.get_actor_id(author_id)
        if not any(a.id == author_id for a in film.authors) :

            film.authors.append(author)
        await self.session.commit()
        await self.session.refresh(film)
        return film
    async def add_list_actor_id(self,actor_ids:list[UUID] ,film_id:UUID)->Film|None:
        film = await self.get_model_id(film_id)
        if not film :
            return None 
        actor_repo= ActorRepository(self.session)
        actors = []
        for actor_id in actor_ids:

            actor =   await actor_repo.get_model_id(actor_id)
            if actor:
                actors.append(actor)
        not_actor_id = {a.id for a in film.authors}
        for actor in actors:
           if actor.id not in  not_actor_id:
               film.actors.append(actor)


            
        await self.session.commit()
        await self.session.refresh(film)
        return film
    async def add_list_author_id(self,author_ids:list[UUID] ,film_id:UUID)->Film|None:
        film = await self.get_film_id(film_id)
        if not film :
            return None 
        actor_repo= AuthorRepository(self.session)
        authors = []
        for author_id in author_ids:

            author =   await actor_repo.get_model_id(author_id)
            if author:
                authors.append(author)
        not_author_id = {a.id  for a in film.authors}
        for author in authors:
           if author.id not in  not_author_id:
               film.authors.append(author)


            
        await self.session.commit()
        await self.session.refresh(film)
        return film   
   
    async def get_film_title(self,film_titel)->Film:
        smt = select(Film).where(Film.title==film_titel)
        relutt = await self.session.execute(smt)
        films = relutt.scalars().first()
        return films
    
    
    

