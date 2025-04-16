from celery.result import AsyncResult
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from redis.asyncio import Redis
from rest_framework import status
from sqlmodel import Session, select

from orm.models import User
from orm.schema import UserCreateResponse
from task_queue.tasks import run_pnet_background, celery_app
from utils.auth import hash_password, verify_password, create_access_token, get_current_user
from utils.database import init_db, get_session
from utils.ip import get_client_ip
from utils.runner import start_server

app = FastAPI()
init_db()

file_Brain_Template = "/home/wsl/anaconda3/envs/pNet/lib/python3.9/site-packages/pnet/Brain_Template/HCP_Surface/Brain_Template.json.zip"
file_scans = "/HCP1200_10Surfs.txt"


@app.on_event("startup")
async def startup():
    redis_uri = "redis://localhost:6379/0"
    redis_connection = Redis.from_url(redis_uri)
    await FastAPILimiter.init(redis_connection)


@app.post("/register/", dependencies=[Depends(RateLimiter(times=5, seconds=60, identifier=get_client_ip))])
async def register(request: Request, session: Session = Depends(get_session)):
    body = await request.json()  # 获取请求体中的 JSON 数据
    username = body.get('username')
    password = body.get('password')

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    # 检查用户名是否已存在
    user_exists = session.exec(select(User).where(User.username == username)).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    # 创建新用户
    user = User(username=username, hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    return UserCreateResponse(
        id=user.id,
        username=user.username,
        url=f"/users/{user.id}"
    )


@app.post("/login/")
async def login(request: Request, session: Session = Depends(get_session)):
    body = await request.json()  # 异步获取请求体
    username = body.get("username")
    password = body.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    user = session.exec(select(User).where(User.username == username)).first()

    # 验证用户名和密码
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 创建访问令牌
    access_token = create_access_token(data={"sub": user.username})

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 3600,
            "user": {
                "id": user.id,
                "username": user.username
            }
        }
    )


@app.post("/run-pnet/")
async def run_pnet_from_config(
        config_file: UploadFile = File(...),
        current_user=Depends(get_current_user)
):
    config_bytes = await config_file.read()
    task = run_pnet_background.delay(config_bytes, config_file.filename)
    return {"status": "submitted", "task_id": task.id}


@app.get("/run-pnet/status/{task_id}")
async def get_pnet_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    response = {
        "task_id": task_id,
        "status": result.status,
    }
    if result.successful():
        response["result"] = result.result
    elif result.failed():
        response["error"] = str(result.result)
    return response


if __name__ == '__main__':
    start_server()
