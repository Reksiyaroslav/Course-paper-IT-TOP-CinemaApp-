from fastapi import Request, Depends
from app.utils.depencines import get_user_service, UserService
from app.scheme.user.model_user import UserResponse


async def get_curen_user(
    request: Request, user_service: UserService = Depends(get_user_service)
) -> UserResponse | None:
    try:
        user_id = request.session.get("user_id")
        if not user_id:
            return None
        user = await user_service.get_user_by_id(user_id)
        print(user)
        return user
    except Exception:
        return None
