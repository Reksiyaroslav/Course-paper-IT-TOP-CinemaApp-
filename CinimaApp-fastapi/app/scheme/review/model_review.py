from typing import Optional
from app.scheme.review.base_review import ReviewBase, ReviewBaseReponse
from app.scheme.user.user_base import UserReponseNotInfo


class CreateReview(ReviewBase):
    pass


class UpdateReview(ReviewBase):
    pass


class ReviewInfo(ReviewBaseReponse):
    user: Optional[UserReponseNotInfo] = None
