import os
import shutil
import tempfile

import pnet
import tomli
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

file_Brain_Template = "/home/wsl/anaconda3/envs/pNet/lib/python3.9/site-packages/pnet/Brain_Template/HCP_Surface/Brain_Template.json.zip"
file_scans = "/HCP1200_10Surfs.txt"


@app.post("/run-pnet/")
async def run_pnet_from_config(config_file: UploadFile = File(...)):
    tmpdir = None  # Initialize tmpdir for cleanup

    try:
        # 使用临时目录保存配置文件
        with tempfile.TemporaryDirectory() as tmpdir:
            # 保存配置文件
            config_path = os.path.join(tmpdir, config_file.filename)
            with open(config_path, "wb") as f:
                shutil.copyfileobj(config_file.file, f)

            # 解析配置文件
            config = read_config(config_path)

            # 从配置中提取参数
            dataType = config['necessary_settings']['dataType']
            dataFormat = config['necessary_settings']['dataFormat']
            dir_pnet_result = config['necessary_settings']['dir_pnet_result']
            file_scans = config['necessary_settings']['file_scans']
            file_Brain_Template = config['necessary_settings']['file_Brain_Template']
            K = config['necessary_settings']['K']
            method = config['necessary_settings']['method']

            if config['pFN_settings']['file_gFN'] == "None":
                file_gFN = None
            else:
                file_gFN = config['pFN_settings']['file_gFN']

            sampleSize = config['gFN_settings']['sampleSize']
            nBS = config['gFN_settings']['nBS']
            nTPoints = config['gFN_settings']['nTPoints']

            pnet_env = config['hpc_settings']['pnet_env']
            hpc_submit = config['hpc_settings']['submit']
            hpc_computation_resource = config['hpc_settings']['computation_resource']

            # 从配置中读取文件路径
            path_template = file_Brain_Template
            path_scans = file_scans
            path_gfn = file_gFN

            # 准备路径和运行
            result_dir = os.path.join(tmpdir, "pnet_result")
            os.makedirs(result_dir, exist_ok=True)

            # 处理是否使用 HPC
            HPC = False  # 这里是设置为 False，实际中你可以根据某些条件来判断

            if not HPC:
                # 在本地执行 pnet.workflow
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
                # 在 HPC 集群上执行 pnet.workflow_cluster
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

            # 返回结果
            return JSONResponse(content={"status": "success", "result_summary": str(result)})

    except Exception as e:
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)

    finally:
        # 确保临时目录被清理
        if tmpdir and os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
            # shutil.rmtree(config['necessary_settings']['dir_pnet_result'])


def read_config(file_path):
    try:
        with open(file_path, "rb") as f:
            config = tomli.load(f)  # , 'owner')
        return config  # necessary_settings, pFN_settings, gFN_settings, hpc_settings
    except tomli.TOMLDecodeError:
        print(f"errors in {file_path}.")
