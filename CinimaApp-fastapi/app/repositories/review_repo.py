from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, and_, or_, select, delete
from math import ceil
from uuid import UUID

from app.db.model.model_db import Review


class ReviewRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_review(self, data: dict, user_id: UUID, film_id: UUID):
        try:
            review = Review(**data, user_id=user_id, film_id=film_id)
            self.session.add(review)
            await self.session.commit()
            await self.session.refresh(review)

            return review
        except SQLAlchemyError as sql_e:
            await self.session.rollback()
            print(f"ERR {sql_e.args}")
            return None

    async def get_list_reviews(self):
        smt = select(Review)
        relult = await self.session.execute(smt)
        reviews = relult.scalars().all()
        return reviews

    async def get_review_by_id(self, review_id: UUID):
        smt = select(Review).where(Review.review_id == review_id)
        relult = await self.session.execute(smt)
        review = relult.scalars().first()
        return review

    async def update_review(self, review_id: UUID, data: dict):
        try:
            review = await self.get_review_by_id(review_id=review_id)
            if not review:
                return None
            for key, value in data.items():
                if value is not None and hasattr(review, key):
                    setattr(review, key, value)
            await self.session.commit()
            await self.session.refresh(review)
            return review
        except SQLAlchemyError:
            await self.session.rollback()
            print("Not update")
            return None

    async def delete_review(self, review_id: UUID) -> bool:
        try:
            smt = delete(Review).where(Review.review_id == review_id)
            await self.session.execute(smt)
            await self.session.commit()
            return True
        except SQLAlchemyError:
            await self.session.rollback()
            print("Not delete")
            return False

    async def avg_corect(self, review_id: UUID):
        review = await self.get_review_by_id(review_id=review_id)
        if not review:
            return None
        total = (
            review.rating_atmosphere
            + review.rating_histrory
            + review.rating_musing
            + review.rating_persons
        )
        review.avg_rating = max((total + 2) // 4, 0)
        await self.session.commit()
        await self.session.refresh(review)
        return review
