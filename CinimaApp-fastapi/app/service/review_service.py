from fastapi import HTTPException
from uuid import UUID
from app.service.base_service import Base_Service
from app.repositories.review_repo import ReviewRepo
from app.repositories.users_repositorie import UserRepository
from app.repositories.films_repositorie import FilmRepository
from app.scheme.review.base_review import ReviewBaseReponse, ReviewBaseList


class ReviewSevice(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.review_repo: ReviewRepo = ReviewRepo(session)
        self.user_repo: UserRepository = UserRepository(session)
        self.film_repo: FilmRepository = FilmRepository(session)

    async def create_review(self, data: dict, user_id: UUID, film_id: UUID):
        user = await self.user_repo.get_user_by_id(user_id=user_id)
        film = await self.film_repo.get_film_by_id(film_id=film_id)
        if not film and not user:
            raise HTTPException(
                status_code=404, detail="Не могут быть пустыми id пользователя и фильма"
            )
        review = await self.review_repo.create_review(
            data=data, user_id=user_id, film_id=film_id
        )
        if review:
            await self.review_repo.avg_corect(review.review_id)
        return ReviewBaseReponse.from_orm(review)

    async def get_list_reviews(self):
        reviews = await self.review_repo.get_list_reviews()
        return ReviewBaseList(reviews=reviews)

    async def get_by_id_review(self, review_id: UUID):
        review = await self.review_repo.get_review_by_id(review_id=review_id)
        return ReviewBaseReponse.from_orm(review)

    async def update_review(self, data: dict, review_id: UUID, film_id: UUID):
        film = await self.film_repo.get_film_by_id(film_id=film_id)
        if not film:
            raise HTTPException(status_code=404, detail="Id фильма не найден")
        update_review = await self.review_repo.update_review(
            review_id=review_id, data=data
        )
        if update_review:
            await self.review_repo.avg_corect(review_id)
            return ReviewBaseReponse.from_orm(update_review)
        raise HTTPException(status_code=500, detail="не удалось обновить рецензию")

    async def delete_review(self, review_id: UUID, film_id: UUID):
        film = await self.film_repo.get_film_by_id(film_id=film_id)
        if not film:
            raise HTTPException(status_code=404, detail="Id фильма не найден")
        bool_sus = await self.review_repo.delete_review(review_id=review_id)
        if bool_sus:
            return "Delete"
        raise HTTPException(status_code=500, detail="Не удалось удалить рецензию")
