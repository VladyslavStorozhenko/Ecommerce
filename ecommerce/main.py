from fastapi import FastAPI
from ecommerce.user import router as user_router
from ecommerce.products import router as product_router
from ecommerce.cart import router as cart_router
from ecommerce.orders import router as orders_router
from ecommerce.auth import router as auth_router
import uvicorn


app = FastAPI(title='EcommerceApp')

app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(cart_router.router)
app.include_router(orders_router.router)
app.include_router(auth_router.router)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0")
