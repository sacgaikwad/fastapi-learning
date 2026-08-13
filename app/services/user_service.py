from app.models.user import UserRequest, UserResponse


def create_user(user: UserRequest) -> UserResponse:

    # Business logic

    # Save to database

    return UserResponse(
        user_id=1
    )