import os
import shutil
import tempfile

import pnet
from celery import Celery

from utils.config_parser import read_config

celery_app = Celery(
    "pnet_tasks",
    broker="redis://localhost:6379/0",
)


@celery_app.task
def run_pnet_background(config_bytes: bytes, config_filename: str):
    tmpdir = None
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, config_filename)
            with open(config_path, "wb") as f:
                f.write(config_bytes)

            config = read_config(config_path)

            data_type = config['necessary_settings']['dataType']
            data_format = config['necessary_settings']['dataFormat']
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
            HPC = False

            if not HPC:
                result = pnet.workflow(
                    dir_pnet_result=dir_pnet_result,
                    dataType=data_type,
                    dataFormat=data_format,
                    file_Brain_Template=file_Brain_Template,
                    file_scan=file_scans,
                    file_subject_ID=None,
                    file_subject_folder=None,
                    file_gFN=file_gFN,
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
                    dataType=data_type,
                    dataFormat=data_format,
                    file_Brain_Template=file_Brain_Template,
                    file_scan=file_scans,
                    file_subject_ID=None,
                    file_subject_folder=None,
                    file_gFN=file_gFN,
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

            return str(result)

    except Exception as e:
        return {"status": "failure", "message": str(e)}

    finally:
        # 确保临时目录被清理
        if tmpdir and os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
