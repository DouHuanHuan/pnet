import os
import shutil
import tempfile

import pnet
import uvicorn
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
from utils.auth import hash_password, verify_password, create_access_token, get_current_user
from utils.config_parser import read_config
from utils.database import init_db, get_session
from utils.ip import get_client_ip

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
    tmpdir = None

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, config_file.filename)
            with open(config_path, "wb") as f:
                shutil.copyfileobj(config_file.file, f)

            config = read_config(config_path)

            dataType = config['necessary_settings']['dataType']
            dataFormat = config['necessary_settings']['dataFormat']
            dir_pnet_result = config['necessary_settings']['dir_pnet_result']
            file_scans = config['necessary_settings']['file_scans']
            file_Brain_Template = config['necessary_settings']['file_Brain_Template']
            K = config['necessary_settings']['K']
            method = config['necessary_settings']['method']
            file_gFN = config['pFN_settings']['file_gFN']
            file_gFN = None if file_gFN == "None" else file_gFN

            sampleSize = config['gFN_settings']['sampleSize']
            nBS = config['gFN_settings']['nBS']
            nTPoints = config['gFN_settings']['nTPoints']

            pnet_env = config['hpc_settings']['pnet_env']
            hpc_submit = config['hpc_settings']['submit']
            hpc_computation_resource = config['hpc_settings']['computation_resource']

            path_template = file_Brain_Template
            path_scans = file_scans
            path_gfn = file_gFN

            result_dir = os.path.join(tmpdir, "pnet_result")
            os.makedirs(result_dir, exist_ok=True)

            HPC = False

            if not HPC:
                result = pnet.workflow(
                    dir_pnet_result=dir_pnet_result,
                    dataType=dataType,
                    dataFormat=dataFormat,
                    file_Brain_Template=path_template,
                    file_scan=path_scans,
                    file_subject_ID=None,
                    file_subject_folder=None,
                    file_gFN=path_gfn,
                    K=K,
                    Combine_Scan=False,
                    method=method,
                    init='random',
                    sampleSize=sampleSize,
                    nBS=nBS,
                    nTPoints=nTPoints,
                    Computation_Mode='CPU_Torch'
                )
            else:
                result = pnet.workflow_cluster(
                    dir_pnet_result=dir_pnet_result,
                    dataType=dataType,
                    dataFormat=dataFormat,
                    file_Brain_Template=path_template,
                    file_scan=path_scans,
                    file_subject_ID=None,
                    file_subject_folder=None,
                    file_gFN=path_gfn,
                    K=K,
                    Combine_Scan=False,
                    method=method,
                    init='random',
                    sampleSize=sampleSize,
                    nBS=nBS,
                    nTPoints=nTPoints,
                    Computation_Mode='CPU_Torch',
                    dir_env=pnet_env['dir_env'],
                    dir_python=pnet_env['dir_python'],
                    dir_pnet=pnet_env['dir_pnet'],
                    submit_command=hpc_submit['submit_command'],
                    thread_command=hpc_submit['thread_command'],
                    memory_command=hpc_submit['memory_command'],
                    log_command=hpc_submit['log_command'],
                    computation_resource=hpc_computation_resource
                )

            return JSONResponse(content={"status": "success", "result_summary": str(result)})

    except Exception as e:
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)

    finally:
        if tmpdir and os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)


if __name__ == '__main__':
    '''
    curl -X POST "http://127.0.0.1:8000/run-pnet/" \
    -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0NDcwMjQyOX0.gKr4D-yKHEIJhSqO-xnAfY8uM2kvzH7SrNuSyv2MrBI" \
    -F "config_file=@/home/wsl/project/pnet/data/fmri_surf_hcp10subjs.toml" \
    --max-time 600
    '''
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        timeout_keep_alive=120
    )
