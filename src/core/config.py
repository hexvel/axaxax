import os

from dotenv import load_dotenv

load_dotenv()


class ProjectConfig:
    BASE_URL = os.getenv("BASE_URL")
    MODEL_USER = "database.models.user"


TORTOISE_ORM = {
    "connections": {"default": ProjectConfig.BASE_URL},
    "apps": {
        "models": {
            "models": [ProjectConfig.MODEL_USER, "aerich.models"],
            "default_connection": "default",
        },
    },
}
