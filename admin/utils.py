import psutil
import shutil
import platform
import time


def get_system_info():

    disk = shutil.disk_usage("/")

    return {

        "cpu": psutil.cpu_percent(interval=1),

        "ram_percent": psutil.virtual_memory().percent,

        "ram_used": round(psutil.virtual_memory().used / (1024**3),2),

        "ram_total": round(psutil.virtual_memory().total / (1024**3),2),

        "disk_percent": psutil.disk_usage("/").percent,

        "disk_free": round(disk.free/(1024**3),2),

        "python": platform.python_version(),

        "uptime": time.time()-psutil.boot_time()

    }
