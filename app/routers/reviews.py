from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.db_depends import get_async_db
from app.models.products import Product as ProductModel
from app.models.reviews import Review as ReviewModel
from app.schemas import Review as ReviewSchema
from app.schemas import ReviewCreate
from app.schemas import User as UserSchema

router = APIRouter(prefix="/reviews", tags=["reviews"])

from sqlalchemy.sql import func


async def update_product_rating(db: AsyncSession, product_id: int):
    """
    Делает пересчет рейтинга товара
    """
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id, ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(ProductModel, product_id)
    product.rating = avg_rating
    await db.commit()


@router.get("/", response_model=list[ReviewSchema])
async def get_reviews(db: Annotated[AsyncSession, Depends(get_async_db)]):
    """
    Получение списка всех активных отзывов
    """
    result = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True))
    reviews = result.all()
    return reviews


@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate,
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_async_db)],
):
    """
    Создает новый отзыв
    """
    # Проверка роли пользователя
    if current_user.role != "buyer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only buyer can post reviews",
        )

    # Проверка существования товара
    result = await db.scalars(
        select(ProductModel).where(
            ProductModel.id == review.product_id, ProductModel.is_active == True
        )
    )
    product_db = result.first()
    if not product_db:
        raise HTTPException(status_code=400, detail="Product not found or inactive")

    # Создание нового отзыва
    review_db = ReviewModel(**review.model_dump(), user_id=current_user.id)
    db.add(review_db)
    await db.commit()
    await db.refresh(review_db)

    # Обновление среднего рейтинга
    await update_product_rating(db, product_db.id)

    return review_db
