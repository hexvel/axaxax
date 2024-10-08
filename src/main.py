import os
import tracemalloc
from tortoise import Tortoise
from fastapi import FastAPI
from loguru import logger
from core.config import TORTOISE_ORM
from database.models.user import User
from services.user import UserService


tracemalloc.start()
logger.disable("vkbottle")


async def statup_tortoise():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    logger.info("Tortoise successfully generate all models.")


async def startup_users():
    users = await User.all()

    if not users:
        logger.warning("Users list is empty.")
        return

    for user in users:
        service = UserService(user)
        await service.start_user_session()


async def lifespan(app: FastAPI):
    os.system("cls")
    await statup_tortoise()
    await startup_users()
    yield
    await Tortoise.close_connections()
    logger.warning("App stopped...")


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="127.0.0.1", port=8000, log_level="warning")
