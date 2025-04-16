import subprocess
import sys

import uvicorn


def start_server():
    """
    curl -X POST "http://127.0.0.1:8000/run-pnet/" \
    -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0NDcwMjQyOX0.gKr4D-yKHEIJhSqO-xnAfY8uM2kvzH7SrNuSyv2MrBI" \
    -F "config_file=@/home/wsl/project/pnet/data/fmri_surf_hcp10subjs.toml" \
    --max-time 600
    """
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        timeout_keep_alive=120
    )

    start_celery_worker()


def start_celery_worker():
    celery_command = [sys.executable, "-m", "celery", "-A", "task_queue.tasks..celery_app", "worker", "--loglevel=info"]
    subprocess.Popen(celery_command)
