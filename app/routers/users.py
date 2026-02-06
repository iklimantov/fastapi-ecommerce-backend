from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db_depends import get_async_db
from app.schemas import User as UserSchema, UserCreate
from app.models.users import User as UserModel
from app.auth import hash_password


router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_async_db)]):
    """
    Регистрирует нового пользователя с ролью 'buyer' или 'seller'.
    """

    # Проверка уникальности email
    email_temp = await db.scalars(select(UserModel).where(UserModel.email == user.email))
    if email_temp.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    # Создание объекта пользователя с хешированным паролем
    db_user = UserModel(email=user.email,
                        hashed_password=hash_password(user.password),
                        role=user.role)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
