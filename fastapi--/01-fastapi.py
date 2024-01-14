#!/usr/bin/env python3
# coding=utf-8
# date 2024-01-14 22:14:28
# author calllivecn <c-all@qq.com>

from typing import (
    Annotated,
    List,
)

from fastapi import (
    FastAPI,
    APIRouter,
    Header,
    Request,
    Response,
    status,
    File,
    UploadFile,
    Depends,
    HTTPException,
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.testclient import TestClient
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from pydantic import BaseModel

app = FastAPI()


@app.get("/favicon.ico")
async def icon():

    return {"message": "Hello World"}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, req: Request, res: Response):
    print(f"{req.headers=}")
    print(f"{res.headers=}")
    res.headers["X-zx-diy"] = "what that is."
    res.status_code = status.HTTP_202_ACCEPTED
    return {"item_id": item_id}



fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]



class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# 这是把 Item 声明为参数
# curl -v -X POST -H "Content-Type: application/json" -d '{"name":"zx", "price": 1.2}' "http://10.1.3.1:8000/items2/"
@app.post("/items2/", response_model=Item, response_model_exclude_unset=True)
async def create_item(item: Item):
    return item



@app.get("/ip")
async def ip(Host: Annotated[str|None, Header()] = None):
    return {"你的ip": Host}


# 这是上传单个文件
@app.post("/file/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    print(f"{file=}")
    return {"filename": file.filename}


# 这是上传多个文件
@app.post("/files/")
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/filemain/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)



class User(BaseModel):
    username: str
    password: str
    email: str|None = None


class UserInDB(User):
    hashed_password: str


user_db = {
    "calllivecn": User(username="calllivecn", password="password-token").model_dump(),
    "user2": User(username="user2", password="password-token").model_dump(),
}
print(f"{user_db=}")

def get_user(token: str):
    if token in user_db:
        return user_db[token]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = user_db.get(token)
    if user:
        user_info = UserInDB(**user, hashed_password="hash_password")
        return user_info
    else:
        raise HTTPException(status_code=400, detail="用户名或密码错误")


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_db.get(form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    user = User(**user)

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_user_info(u: User = Depends(get_current_user)):
    return u



app.mount("/static", StaticFiles(directory="static", html=True), name="static")




# 测试

client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"Hello World"}
