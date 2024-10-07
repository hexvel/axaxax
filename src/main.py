from tortoise import Tortoise
from fastapi import FastAPI
from loguru import logger
from app.core.config import TORTOISE_ORM


async def statup_tortoise():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    logger.info("Tortoise successfully generate all models.")


async def lifespan(app: FastAPI):
    await statup_tortoise()
    yield
    logger.warning("App stopped...")


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="127.0.0.1", port=8000, log_level="warning")
