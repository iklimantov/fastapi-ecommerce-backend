from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.db_depends import get_db
from app.models.categories import Category as CategoryModel
from app.schemas import Category as CategorySchema
from app.schemas import CategoryCreate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategorySchema])
async def get_all_categories(db: Session = Depends(get_db)):
    """
    Возвращает список всех активных категорий.
    """
    stmt = select(CategoryModel).where(CategoryModel.is_active == True)
    categories = db.scalars(stmt).all()
    return categories


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Создаёт новую категорию.
    """
    # Проверка существования parent_id, если указан
    if category.parent_id is not None:
        stmt = select(CategoryModel).where(
            CategoryModel.id == category.parent_id, CategoryModel.is_active == True
        )
        parent = db.scalars(stmt).first()
        if parent is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Parent model not found"
            )

    # Создание новой категории
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.put("/")
async def mark_all_categories_as_active(db: Session = Depends(get_db)):
    """
    Присваивает всем категориям статус активных
    """
    db.execute(
        update(CategoryModel)
        .where(CategoryModel.is_active == False)
        .values(is_active=True)
    )
    db.commit()
    return {"message": "All categories marked as active"}


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(
    category_id: int, category: CategoryCreate, db: Session = Depends(get_db)
):
    """
    Обновляет категорию по её ID.
    """
    # Проверка существования категории
    stmt = select(CategoryModel).where(
        CategoryModel.id == category_id, CategoryModel.is_active == True
    )
    db_category = db.scalars(stmt).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    # Проверка parent id
    if category.parent_id is not None:
        stmt = select(CategoryModel).where(
            CategoryModel.id == category.parent_id, CategoryModel.is_active == True
        )

        parent = db.scalars(stmt).first()
        if parent is None:
            raise HTTPException(status_code=400, detail="Parent category not found")

    # Обновление категории
    db.execute(
        update(CategoryModel)
        .where(CategoryModel.id == category_id)
        .values(**category.model_dump())
    )
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Логически удаляет категорию по её ID, устанавливая is_active=False.
    """
    # Проверка наличия активной категории
    stmt = select(CategoryModel).where(
        CategoryModel.id == category_id, CategoryModel.is_active == True
    )
    category = db.scalars(stmt).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    # Логическое удаление категории (Установка is_active = False)
    db.execute(
        update(CategoryModel)
        .where(CategoryModel.id == category_id)
        .values(is_active=False)
    )
    db.commit()

    return {"status": "success", "message": "Category marked as inactive"}
