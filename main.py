# main.py
import os
import shutil
import tempfile

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from config_parser import parse_config
from workflow_runner import run_pnet_workflow

app = FastAPI()


@app.post("/run-pnet/")
async def run_pnet_from_config(
        config_file: UploadFile = File(...),
        file_Brain_Template: UploadFile = File(...),
        file_scans: UploadFile = File(...),
        file_gFN: UploadFile = File(...)
):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # 保存 TOML 配置文件
            config_path = os.path.join(tmpdir, config_file.filename)
            with open(config_path, "wb") as f:
                shutil.copyfileobj(config_file.file, f)

            config = parse_config(config_path)

            # 保存其他输入文件
            path_template = os.path.join(tmpdir, file_Brain_Template.filename)
            with open(path_template, "wb") as f:
                shutil.copyfileobj(file_Brain_Template.file, f)

            path_scans = os.path.join(tmpdir, file_scans.filename)
            with open(path_scans, "wb") as f:
                shutil.copyfileobj(file_scans.file, f)

            path_gfn = os.path.join(tmpdir, file_gFN.filename)
            with open(path_gfn, "wb") as f:
                shutil.copyfileobj(file_gFN.file, f)

            # 准备 paths 和运行
            result_dir = os.path.join(tmpdir, "pnet_result")
            os.makedirs(result_dir, exist_ok=True)

            paths = {
                "template": path_template,
                "scan": path_scans,
                "gfn": path_gfn
            }

            result = run_pnet_workflow(config, paths, result_dir)

            return JSONResponse(content={"status": "success", "result_summary": str(result)})
    except Exception as e:
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)
