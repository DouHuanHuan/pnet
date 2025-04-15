import os

from loguru import logger

# 日志目录
log_dir = "../logs"
os.makedirs(log_dir, exist_ok=True)

# 配置 loguru
logger.add(
    os.path.join(log_dir, "audit.log"),
    rotation="10 MB",  # 超过 10MB 自动切割
    retention="7 days",  # 最多保留 7 天
    compression="zip",  # 旧日志压缩
    encoding="utf-8",
    enqueue=True,  # 支持多线程多进程安全写入
    backtrace=True,  # 捕获堆栈
    diagnose=True,  # 捕获变量
    level="INFO"
)
