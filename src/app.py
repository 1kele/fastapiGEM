import sys
from fastapi import FastAPI, APIRouter

from src.exception_handlers import not_found_handler
from src.exceptions.base import NotFoundError
from src.routers.gem_type import router as gem_type_router
from src.routers.request import router as request_router

from loguru import logger

logger.remove()

logger.configure(
    handlers=[
        # Handler А: Красивый цветной вывод в консоль
        {
            "sink": sys.stdout,
            "level": "DEBUG",
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            "colorize": True,
        },
        # Handler Б: Запись критических ошибок в файл + ротация + сжатие
        {
            "sink": "logs/errors.log",
            "level": "ERROR",
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            "rotation": "10 MB",  # Создать новый файл, когда этот достигнет 10 МБ
            "retention": "10 days",  # Хранить логи только за последние 10 дней
            "compression": "zip",  # Старые архивировать в .zip для экономии места
            "encoding": "utf-8",
        },
    ]
)


app = FastAPI()

app.add_exception_handler(NotFoundError, not_found_handler)

app.include_router(gem_router)
app.include_router(gem_type_router)
app.include_router(request_router)