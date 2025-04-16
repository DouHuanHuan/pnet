import subprocess
import sys
from multiprocessing import Process

import uvicorn


def start_server():
    """
    curl -X POST "http://127.0.0.1:8000/run-pnet/" \
    -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0NDc3NjcyOX0.pC-QVs5OfLbaKv15sq7ZfuGcwWVNYV06ufErGxaN71I" \
    -F "config_file=@/home/wsl/project/pnet/data/fmri_surf_hcp10subjs.toml" \
    --max-time 600
    """
    Process(target=start_fastapi).start()
    Process(target=start_celery).start()


def start_fastapi():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


def start_celery():
    subprocess.run([sys.executable, "-m", "celery", "-A", "task_queue.tasks.celery_app", "worker", "--loglevel=info"])
