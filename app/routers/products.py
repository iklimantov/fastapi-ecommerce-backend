from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.db_depends import get_db
from app.models import Category as CategoryModel
from app.models import Product as ProductModel
from app.schemas import Product as ProductSchema
from app.schemas import ProductCreate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductSchema])
async def get_all_products(db: Session = Depends(get_db)):
    """
    Возвращает список всех товаров.
    """
    stmt = (
        select(ProductModel)
        .join(CategoryModel)
        .where(ProductModel.is_active == True, CategoryModel.is_active == True)
    )
    return db.scalars(stmt).all()


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Создаёт новый товар.
    """
    # Проверка существования категории, к которой относится товар
    stmt = select(CategoryModel).where(
        CategoryModel.id == product.category_id, CategoryModel.is_active == True
    )
    category = db.scalars(stmt).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found or inactive",
        )

    # Создание нового продукта
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/category/{category_id}", response_model=list[ProductSchema])
async def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    """
    Возвращает список товаров в указанной категории по её ID.
    """
    # Проверка существования категории
    stmt = select(CategoryModel).where(
        CategoryModel.id == category_id, CategoryModel.is_active == True
    )
    category = db.scalars(stmt).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found or inactive")

    stmt = select(ProductModel).where(
        ProductModel.category_id == category_id, ProductModel.is_active == True
    )
    products = db.scalars(stmt).all()
    return products


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Возвращает детальную информацию о товаре по его ID.
    """
    stmt = select(ProductModel).where(
        ProductModel.id == product_id, ProductModel.is_active == True
    )
    product = db.scalars(stmt).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    stmt = select(CategoryModel).where(
        CategoryModel.id == product.category_id, CategoryModel.is_active == True
    )
    category = db.scalars(stmt).first()
    if category is None:
        raise HTTPException(status_code=400, detail="Category not found or inactive")

    return product


@router.put("/")
async def mark_all_products_as_active(db: Session = Depends(get_db)):
    """
    Присваивает всем продуктам статус активных
    """
    db.execute(
        update(ProductModel)
        .where(ProductModel.is_active == False)
        .values(is_active=True)
    )
    db.commit()
    return {"message": "All products marked as active"}


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int, product: ProductCreate, db: Session = Depends(get_db)
):
    """
    Обновляет товар по его ID.
    """
    # Проверка существования товара
    stmt = select(ProductModel).where(
        ProductModel.id == product_id, ProductModel.is_active == True
    )
    product_db: ProductModel | None = db.scalars(stmt).first()
    if product_db is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # Проверка существования категории
    stmt = select(CategoryModel).where(CategoryModel.id == product.category_id)
    category = db.scalars(stmt).first()
    if category is None:
        raise HTTPException(status_code=400, detail="Category not found or inactive")

    # Обновление товара
    stmt = (
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(**product.model_dump())
    )
    db.execute(stmt)
    db.commit()
    db.refresh(product_db)
    return product_db


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Удаляет товар по его ID.
    """
    # Проверка существования товара
    stmt = select(ProductModel).where(
        ProductModel.id == product_id, ProductModel.is_active == True
    )
    product: ProductModel | None = db.scalars(stmt).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.execute(
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(is_active=False)
    )
    db.commit()
    return {
        "status": "success",
        "message": f"Product {product.name}, id={product_id} marked as inactive",
    }
