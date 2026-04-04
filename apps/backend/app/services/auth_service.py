from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.db.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import TokenResponse, UserLogin, UserPublic, UserRegister


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.users = UserRepository(db)

    async def register(self, data: UserRegister) -> TokenResponse:
        email = data.email.strip().lower()
        if await self.users.get_by_email(email) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists",
            )

        user = User(
            email=email,
            full_name=data.name,
            hashed_password=hash_password(data.password),
        )
        user = await self.users.create(user)
        return self._token_response(user)

    async def login(self, data: UserLogin) -> TokenResponse:
        email = data.email.strip().lower()
        user = await self.users.get_by_email(email)
        if user is None or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        return self._token_response(user)

    def _token_response(self, user: User) -> TokenResponse:
        token = create_access_token(
            subject=str(user.id),
            email=user.email,
        )
        return TokenResponse(
            access_token=token,
            user=UserPublic.model_validate(user),
        )
