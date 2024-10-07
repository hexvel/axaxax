from fastapi import FastAPI
from loguru import logger


async def lifespan(app: FastAPI):
    logger.debug("App started...")
    yield
    logger.warning("App stopped...")


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="127.0.0.1", port=8000, log_level="warning")
