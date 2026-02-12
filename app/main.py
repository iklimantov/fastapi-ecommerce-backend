from fastapi import FastAPI, HTTPException

from app.routers import categories, products, reviews, users

app = FastAPI(title="Ecommerce App", version="1.0.0")

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(reviews.router)


@app.get("/")
async def root(num: int = 0):
    """
    Корневой маршрут, подтверждающий, что API работает.
    Возвращает пароль главного администратора пентагона при запросе числа 47.
    """
    if num == 47:
        raise HTTPException(
            status_code=418,
            detail="I'm a teapot. I can't hack the Pentagon because I don't have paws.",
        )
    return {"message": "Добро пожаловать в API интернет-магазина!"}
