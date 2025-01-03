from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from typing import List


app = FastAPI()
users = {}


class Order(BaseModel):
    name_product: str
    amount: int = Field(ge=0, default=0)
    price: float


class User(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    product_list: List[Order]


@app.post('/add')
async def add_new_user(user: User):
    users[user.email] = {'name': user.name,
                         'product_list': user.product_list}


@app.get('/get')
async def get_all_info_user_by_email(email: EmailStr):
    return users[email]


