from typing import Annotated
from fastapi import FastAPI, HTTPException, Request, Path
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse


app = FastAPI(swagger_ui_parameters={"tyItOuyEnable": True}, debug=True)
templates = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: int = Field(ge=1, le=100, description='Enter User ID')
    username: str = Field(min_length=3, max_length=20, description='Enter Username')
    age: int = Field(ge=18, le=100, description='Enter User age')

# class UserCreate(BaseModel):
#     id: int = Field(ge=1, le=100, description='Enter User ID')
#     username: str = Field(min_length=3, max_length=20, description='Enter Username')
#     age: int = Field(ge=18, le=100, description='Enter User age')



@app.get('/', response_class=HTMLResponse)
async def get_all_users(request: Request):
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/user/{user_id}', response_class=HTMLResponse)
async def get_users(request: Request, user_id: Annotated[int, Path(ge=1)]):
    try:
        return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.post('/user/{username}/{age}', response_class=HTMLResponse)
async def create_user(request: Request,
                      username: Annotated[str, Path(min_length=3, max_length=20, description='Enter Username')],
                      age: Annotated[int, Path(ge=18, le=100, description='Enter User age')]):
    new_id = max(user.id for user in users) + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.put('/user/{user_id}/{username}/{age}', response_class=HTMLResponse)
async def update_user(request: Request,
                      user_id: int,
                      username: Annotated[str, Path(min_length=3, max_length=20, description='Enter Username')],
                      age: Annotated[int, Path(ge=18, le=100, description='Enter User age')]):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return templates.TemplateResponse('users.html', {'request': request, 'users': users})
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}', response_class=HTMLResponse)
async def delete_user(request: Request, user_id: Annotated[int, Path(ge=1, le=100)]):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return templates.TemplateResponse('users.html', {'request': request, 'users': users})
    raise HTTPException(status_code=404, detail='User was not found')