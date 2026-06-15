import logging
import os

os.makedirs("logs", exist_ok=True)

log_format = "%(asctime)s - %(levelname)s - %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler("logs/app.log", encoding="utf-8"),  
        logging.StreamHandler()                               
    ]
)

logger = logging.getLogger("library_api")