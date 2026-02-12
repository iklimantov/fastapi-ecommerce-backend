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

# teapot = status.HTTP_418_IM_A_TEAPOT


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
    Создает новый отзыв (только для "buyer")
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

    # Проверка, что пользователь еще не оставлял отзыв на этот товар
    result = await db.scalars(
        select(ReviewModel).where(
            ReviewModel.user_id == current_user.id,
            ReviewModel.product_id == product_db.id,
            ReviewModel.is_active == True,
        )
    )
    if result.first():
        raise HTTPException(
            status_code=400, detail="Users can post only one review for the product"
        )

    # Создание нового отзыва
    review_db = ReviewModel(**review.model_dump(), user_id=current_user.id)
    db.add(review_db)
    await db.commit()
    await db.refresh(review_db)

    # Обновление среднего рейтинга
    await update_product_rating(db, product_db.id)

    return review_db


@router.delete("/reviews/{review_id}")
async def delete_review(
    review_id: int,
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_async_db)],
):
    """
    Удаляет отзыв по его id.
    Доступно пользователю, написавшему отзыв, или администратору
    """
    # Проверка роли пользователя
    if current_user.role not in ("admin", "buyer"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
        )

    # Проверка существования отзыва
    result = await db.scalars(
        select(ReviewModel).where(
            ReviewModel.id == review_id, ReviewModel.is_active == True
        )
    )
    review_db = result.first()
    if not review_db:
        raise HTTPException(status_code=404, detail="Review not found or inactive")

    # Проверка авторства пользователя
    if current_user.role == "buyer" and current_user.id != review_db.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Users can only delete their own reviews",
        )

    # Мягкое удаление отзыва
    review_db.is_active = False
    await db.commit()

    # Обновление рейтинга товара
    await update_product_rating(db, review_db.product_id)

    return {"message": "Review deleted"}
